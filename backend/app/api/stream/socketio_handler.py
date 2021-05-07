import paho.mqtt.client as mqtt
import socketio
from datetime import datetime
import sys
sys.path.append("/home/ducdv10/Documents/do_an/backend/")
import json
from app.config import DroneDetectionConfig as cf
from app.extensions import load_bytes_from_redis, load_frame_from_redis
from app.extensions import red
import logging

logging.basicConfig(format=cf.LOGGING_FORMAT, datefmt=cf.LOGGING_DATEFMT, level=cf.LOGGING_LEVEL)

LAST_SEND = 0

sio = socketio.Client()
sio.connect('http://localhost:4321')
logging.info("Connected socket.io SID is {}".format(sio.sid))


class Extrapolator(object):
    def __init__(self, enable=False):
        zero_detection = {'timestamp': 0,
                          'boxes': [],
                          'scores': [],
                          "classes": []
                          }
        self.MIN_SCORE = 0.1
        self.D_THRESH = 0.02
        self.enabled = enable
        self.previous = zero_detection
        self.current = zero_detection
        self.matched_objects = []

    def _get_objects(self, detection):
        objects = []
        ob = {}
        for i in range(len(detection['classes'])):
            ob['class'] = detection['classes'][i]
            ob['score'] = detection['scores'][i]
            ob['box'] = detection['boxes'][i]
            ob['x'] = ob['box'][2] - ob['box'][0]
            ob['y'] = ob['box'][3] - ob['box'][1]
            ob['timestamp'] = detection['timestamp']
            objects.append(ob)
        return objects

    def _find_closest_object(self, cob, pobs):
        idx = -1
        dis = 10
        for i, pob in enumerate(pobs):
            if cob['class'] == pob['class']:
                # check cob and pob close enough:
                if dis > max(abs(cob['x'] - pob['x']), abs(cob['y'] - pob['y'])):
                    dis = max(abs(cob['x'] - pob['x']), abs(cob['y'] - pob['y']))
                    idx = i
        if dis < self.D_THRESH:
            return idx
        else:
            return -1

    def match_objects(self):
        """
        check all drone class 0 object in current
        if same class, in a limit distance => match the closest, add matched, and remove the matched
            if not in limit distance => remove the object in current
        return matched
        """
        self.matched_objects = []
        current_objects = self._get_objects(self.current)
        previous_objects = self._get_objects(self.previous)
        for cob in current_objects:
            idx = self._find_closest_object(cob, previous_objects)
            if idx > -1:
                self.matched_objects.append([cob.copy(), previous_objects[idx].copy()])
                # equivalent remove matched object in previous objects
                previous_objects[idx]['class'] = -1

    def update_detection(self, new_detection):
        self.previous = self.current
        self.current = new_detection
        # TODO: Reset matched_objects each new detection (even no detection?)
        if self.enabled:
            self.match_objects()

    def _calculate_box_score_class(self, cob, pob, timestamp):
        t0 = cob['timestamp']
        t1 = pob['timestamp']
        delta_t = t0 - t1
        box = [0, 0, 0, 0]
        # TODO: min 0, max 1
        for i in range(4):
            box[i] = (cob['box'][i] - pob['box'][i]) / delta_t * (timestamp - t1) + pob['box'][i]
        score = (cob['score'] - pob['score']) / delta_t * (timestamp - t1) + pob['score']
        return box, score, cob['class']

    def _extrapolate_detection(self, timestamp):
        boxes = []
        scores = []
        classes = []
        for matched_ob in self.matched_objects:
            cob = matched_ob[0]
            pob = matched_ob[1]
            box, score, classs = self._calculate_box_score_class(cob, pob, timestamp)
            boxes.append(box)
            scores.append(score)
            classes.append(classs)
        return {'boxes': boxes, 'scores': scores, 'classes': classes, 'timestamp': timestamp}

    def extrapolate(self, timestamp):
        if not self.enabled:
            return self.current.copy()
        else:
            # # TODO: AI here. Experiment
            if timestamp <= self.previous['timestamp']:
                return self.previous.copy()
            if timestamp >= self.current['timestamp']:
                return self.current.copy()
            return self._extrapolate_detection(timestamp)


AI = Extrapolator(cf.EXTRAPOLATION_ENABLED)


def send_frame(client, userdata, msg):
    global LAST_SEND
    global AI
    json_payload = json.loads(msg.payload)
    pub_timestamp = json_payload["timestamp"]

    # Not need to proceed stack in further past
    if pub_timestamp - LAST_SEND < 0.1:
        return None
    logging.info("[F-{}] Send frame to socket.io server".format(pub_timestamp))
    # TODO: extrapolation. If not extrapolated, current frame
    # timestamp can be a little ahead with detection timestamp
    frame_dict = load_frame_from_redis(red, cf.NEW_FRAME_REDIS_KEY)
    frame_timestamp = frame_dict["timestamp"]

    detection = AI.extrapolate(frame_timestamp)
    try:
        sio.emit('new_frame_event', {'frame': cf.NEW_FRAME_REDIS_KEY, 'detection': detection, 'room': ""})
        LAST_SEND = datetime.now().timestamp()
    except Exception as e:
        pass


def update_detection(client, userdata, msg):
    """ The callback for when a PUBLISH message is received from the 'update/boxes' Topic  """
    json_payload = json.loads(msg.payload)
    pub_timestamp = json_payload["timestamp"]
    try:
        # boxes_name = msg.payload
        boxes_data = load_bytes_from_redis(red, cf.NEW_DETECTION_REDIS_KEY)  # Load box from redis
        boxes_data = boxes_data.decode('utf8')  # Convert to string
        boxes_data = json.loads(boxes_data)  # Convert to json
        global AI
        AI.update_detection(boxes_data)
    except Exception as e:
        pass


client = mqtt.Client("socketio_handler")  # Create instance of client with client ID ...
client.connect(cf.BROKER_HOST, cf.BROKER_PORT)  # Connect to broker
client.subscribe(cf.UPDATE_FRAME_TOPIC)  # Subscribe to "update/frame" topic
client.message_callback_add(cf.UPDATE_FRAME_TOPIC, send_frame)  # Callback to send_frame method
client.subscribe(cf.UPDATE_BOXES_TOPIC)  # Subscribe to "update/boxes" topic
client.message_callback_add(cf.UPDATE_BOXES_TOPIC, update_detection)  # Callback to send_boxes method
client.loop_forever()  # Start networking daemon
