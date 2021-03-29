import logging


class DroneDetectionConfig:
    HOST = "0.0.0.0"
    PORT = 4321
    BROKER_HOST = "127.0.0.1"
    BROKER_PORT = 1883
    LEN_LIST_FRAME = 27   # Must be >= (DISTANCE_FRAME * 2 + 1)
    DISTANCE_FRAME = 10   # Distance from first frame to mid frame in stack
    FRAME_SEND_INDEX = 1  # Delay (LEN_LIST_FRAME - DISTANCE_FRAME - FRAME_SEND_INDEX) frame, directly in command line

    NEW_STACK_REDIS_KEY = "stack_redis_key"
    NEW_FRAME_REDIS_KEY = "frame_redis_key"
    NEW_DETECTION_REDIS_KEY = "detection_redis_key"
    FLAG_REDIS_KEY = "flag_detect"

    UPDATE_STACK_TOPIC = "update/stack"
    UPDATE_FRAME_TOPIC = "update/frame"
    UPDATE_BOXES_TOPIC = "update/boxes"

    LOGGING_LEVEL = logging.INFO
    LOGGING_FORMAT = '%(asctime)s - %(process)d - %(levelname)5s - %(message)s'
    LOGGING_DATEFMT = '%d-%b-%y %H:%M:%S'

    EXTRAPOLATION_ENABLED = False




