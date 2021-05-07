import paho.mqtt.client as mqttClient
import time
import cv2
import sys
sys.path.append("/home/ducdv10/Documents/do_an/backend/")
from app.config import DroneDetectionConfig as cf
from app.extensions import save_stack_to_redis, \
                save_frame_to_redis, set_key,stack_frames,red
from datetime import datetime
import json
import threading
import argparse
import sys
import logging

logging.basicConfig(filename="rtsp.log", format=cf.LOGGING_FORMAT, datefmt=cf.LOGGING_DATEFMT)
FRAME_QUEUE = []
TIME_QUEUE = []
TRIAL_CONNECTION_NUM = 1
count = 0


def process_frame(frame,mode):
    logging.info("frame shape: {}".format(frame.shape))
    global FRAME_QUEUE
    global TIME_QUEUE
    global count
    now = count

    if len(FRAME_QUEUE) == cf.LEN_LIST_FRAME:
        FRAME_QUEUE.pop(0)
        TIME_QUEUE.pop(0)
        FRAME_QUEUE.append(frame)
        TIME_QUEUE.append(now)
        # Stack and store new stack
        # TODO: adaptive FRAME_SEND_INDEX => minimize do lech
        STACK_FRAME_INDEX = cf.LEN_LIST_FRAME - cf.DISTANCE_FRAME - 1
        stacked_frame = stack_frames([FRAME_QUEUE[STACK_FRAME_INDEX - cf.DISTANCE_FRAME],
                                    FRAME_QUEUE[STACK_FRAME_INDEX - 1],
                                    FRAME_QUEUE[STACK_FRAME_INDEX],
                                    FRAME_QUEUE[STACK_FRAME_INDEX + 1],
                                    FRAME_QUEUE[STACK_FRAME_INDEX + cf.DISTANCE_FRAME]])
        encoded = cv2.imencode('.jpg', FRAME_QUEUE[cf.FRAME_SEND_INDEX])[1]   # Encode image
        stack_timestamp = TIME_QUEUE[STACK_FRAME_INDEX]
        frame_timestamp = TIME_QUEUE[cf.FRAME_SEND_INDEX]
    # Case 2: Not enough DISTANCE_FRAME*2+1 frame, create stack with 5 same frame
    else:
        FRAME_QUEUE.append(frame)
        TIME_QUEUE.append(now)
        stacked_frame = stack_frames([frame, frame, frame, frame, frame])
        encoded = cv2.imencode('.jpg', frame)[1] # Encode image and store new frame to redis
        stack_timestamp = now
        frame_timestamp = now

    logging.info("encoded shape: {}".format(encoded.shape))
    image_data = encoded.tostring() # Convert to string
    save_stack_to_redis(red, {"stack": stacked_frame, "timestamp": stack_timestamp}, cf.NEW_STACK_REDIS_KEY)
    save_frame_to_redis(red, {"frame": image_data, "timestamp": frame_timestamp}, cf.NEW_FRAME_REDIS_KEY)
    count += 1
    # Need call now again for more precise publish timestamp
        
    now = datetime.now().timestamp()
    stack_payload = json.dumps({"timestamp": now})
    pubsub_client.publish(cf.UPDATE_STACK_TOPIC, stack_payload)

    frame_payload = json.dumps({"timestamp": now})
    pubsub_client.publish(cf.UPDATE_FRAME_TOPIC, frame_payload)
PUBSUB_CONNECTED = False   # global variable for the state of the connection


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        global PUBSUB_CONNECTED  # Use global variable
        PUBSUB_CONNECTED = True  # Signal connection
    else:
        logging.info("FAIL to connect to pub-sub broker.")


pubsub_client = mqttClient.Client("rtsp_daemon")  # create new instance
pubsub_client.on_connect = on_connect  # attach function to callback
pubsub_client.connect(cf.BROKER_HOST, cf.BROKER_PORT)  # connect to broker
pubsub_client.loop_start()
while not PUBSUB_CONNECTED:    # Wait for connection
    time.sleep(0.1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--link", help="IP camera url including username password in RTSP case.")
    parser.add_argument("-v", "--mode", type=int, choices=[0, 1], help="0: run, 1: test")
    args = parser.parse_args()
    link = args.link
    # Mode connection test
    if args.mode == 1:
        logging.info("Test connection to camera using {}.".format(link))
        try:
            success = False
            i = 1
            while not success:
                vcap = cv2.VideoCapture(link)
                success, frame = vcap.read()
                #logging.info("image input shape: {}".format(frame.shape))
                if success:
                    sys.exit(0)
                i = i + 1
                if i > TRIAL_CONNECTION_NUM:
                    success = True
            sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)
    # Mode run
    if args.mode == 0:
        set_key(red,data="TEST")
        logging.info("Create connection to camera using {}.".format(link))
        try:
            success = False
            i = 1
            # Try waiting for keyframe https://stackoverflow.com/questions/15005436/errors-when-decode-h-264-frames-using-ffmpeg
            while not success:
                vcap = cv2.VideoCapture(link)
                preframe_tm = time.time()
                success, frame = vcap.read()
                #logging.info("image input shape: {}".format(frame.shape))
                i = i + 1
                if i > TRIAL_CONNECTION_NUM:
                    success = True
            while True:
                # Read frame
                success, frame = vcap.read()
                elapsed_time = time.time() - preframe_tm
                if elapsed_time < 0.1:
                    continue
                preframe_tm = time.time()
                if success:
                    # See more: need thread here to read stream udp with minimal loss
                    # https://stackoverflow.com/questions/49233433/opencv-read-errorh264-0x8f915e0-error-while-decoding-mb-53-20-bytestream
                    # https://stackoverflow.com/questions/29075467/set-rtsp-udp-buffer-size-in-ffmpeg-libav
                    processing_frame_thread = threading.Thread(target=process_frame, args=(frame,args.mode))
                    processing_frame_thread.start()
        except Exception as e:
            logging.exception("Disconnect to pub-sub broker.")
            pubsub_client.disconnect()
            pubsub_client.loop_stop()