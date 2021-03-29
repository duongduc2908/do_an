import json
from time import sleep, time
from numpy.lib.type_check import imag
import paho.mqtt.client as mqtt
from datetime import datetime
from utils_pro.utils import load_stack_from_redis,load_bytes_from_redis, r
from utils_pro.config import DroneDetectionConfig as cf
from utils_pro.face_goodness_score import angle_score, face_goodness_score
import logging
import pickle
import cv2
import time
from feature_extraction.extractor import FaceVector
from face_detection.face_detection import detect_face


face_vector = FaceVector()

svm_file='models/face_model.pkl'
svm = pickle.load(open(svm_file, 'rb'))
name_file='models/name_model.pkl'
name_model = pickle.load(open(name_file, 'rb'))
font = cv2.FONT_HERSHEY_SIMPLEX


logging.basicConfig(format=cf.LOGGING_FORMAT, datefmt=cf.LOGGING_DATEFMT, level=cf.LOGGING_LEVEL)


def backend_to_model_stack_frame(client, user, message):
    flag_wait = True
    # Help to release all the stack retained in queue before more than 0.1s ago (or should be than 1/fps)
    json_payload = json.loads(message.payload)
    pub_timestamp = json_payload["timestamp"]
    now = datetime.now().timestamp()
    time_check = now - pub_timestamp
    if time_check > 0.1:
        logging.debug("[S-{}] Detect new stack. (skipped)".format(pub_timestamp))
        return None

    logging.debug("[S-{}] Detect new stack".format(pub_timestamp))
    flag_dict = load_bytes_from_redis(r,cf.FLAG_REDIS_KEY).decode('utf-8')
    names = []
    local_image = []
    if flag_dict!="TRAIN":
        stack_dict = load_stack_from_redis(r, cf.NEW_STACK_REDIS_KEY)
        if stack_dict:
            result = stack_dict["stack"]
            stack_timestamp = stack_dict["timestamp"]
            # Predict on stacked image
            # TODO: swap labels: 0:drone, 1:bird, 2:unknown
            image = result[2,:,:,:]
            bbs, points = detect_face(image)
            for bb, point in zip(bbs, points):
                emb=face_vector.get_vector(image, bb,point)		
                y_pred,label = svm.predict([[emb]])
                name=name_model.inverse_transform(label)
                if y_pred[0]>1:
                    name=['']
                names.append(name)
            res = {
                    "boxes": bbs.tolist(),
                    "names": names,
                    "timestamp": stack_timestamp,
                    "local_image": local_image 
                    }
            res = json.dumps(res, indent=2).encode('utf-8')
            r.set(cf.NEW_DETECTION_REDIS_KEY, res)  # FAKE_res or res
            # Need call now again for more precise publish timestamp
            now = datetime.now().timestamp()
            detection_payload = json.dumps({"timestamp": now})
            client_sub.publish(topic=cf.UPDATE_BOXES_TOPIC, payload=detection_payload)
            logging.info("[D-{}] Publish new detection.".format(now))
            print(res)
    else:
        while len(local_image)<3:
            stack_dict = load_stack_from_redis(r, cf.NEW_STACK_REDIS_KEY)
            if stack_dict:
                result = stack_dict["stack"]
                frame_number,frame_height,frame_width,chanel = result.shape
                stack_timestamp = stack_dict["timestamp"]
                # Predict on stacked image
                # TODO: swap labels: 0:personal, 1:unknown

                image = result[2,:,:,:]
                bbs, points = detect_face(image)
                for bb, point in zip(bbs, points):
                    local = angle_score(points)
                    if local == "CENTER" and local_image[0] != None:
                        local_image[0] = True

                    if local == "LEFT" and local_image[1] != None:
                        local_image[1] = True
                    
                    if local == "RIGHT" and local_image[2] != None:
                        local_image[2] = True
                res = {
                            "boxes": bbs.tolist(),
                            "names": names,
                            "timestamp": stack_timestamp,
                            "local_image": local_image 
                        }
                res = json.dumps(res, indent=2).encode('utf-8')
                r.set(cf.NEW_DETECTION_REDIS_KEY, res)  # FAKE_res or res
                # Need call now again for more precise publish timestamp
                now = datetime.now().timestamp()
                detection_payload = json.dumps({"timestamp": now})
                client_sub.publish(topic=cf.UPDATE_BOXES_TOPIC, payload=detection_payload)
                logging.info("[D-{}] Publish new detection.".format(now))
    
            
client_sub = mqtt.Client("model_handler")
client_sub.connect(host=cf.BROKER_HOST, port=cf.BROKER_PORT)
client_sub.subscribe(cf.UPDATE_STACK_TOPIC, qos=0)
client_sub.message_callback_add(cf.UPDATE_STACK_TOPIC, backend_to_model_stack_frame)
client_sub.loop_forever()

