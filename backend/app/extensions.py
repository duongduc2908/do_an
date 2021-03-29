import redis
from flask_socketio import SocketIO
from webargs.flaskparser import FlaskParser
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_redis import FlaskRedis
from logging.handlers import RotatingFileHandler
import pandas
import logging
from app.config import DroneDetectionConfig as cf
import struct
import numpy as np


users_login = {}
logging.basicConfig(format=cf.LOGGING_FORMAT, datefmt=cf.LOGGING_DATEFMT, level=cf.LOGGING_LEVEL)
pd = pandas
parser = FlaskParser()
jwt = JWTManager()
client = PyMongo()
redis_store = FlaskRedis()
app_log_handler = RotatingFileHandler('logs/app.log', maxBytes=1000000, backupCount=30)
red = redis.StrictRedis(host='localhost',port=6379, db=0)
socketio = SocketIO(cors_allowed_origins='*')


def save_bytes_to_redis(red, encoded, name):
    """Store given image encoded in bytes in redis"""
    red.set(name, encoded)
    return


def load_bytes_from_redis(red, name):
    """Retrieve image encoded in bytes from Redis key"""
    encoded = red.get(name)
    return encoded


def save_numpy_to_redis(red, array, name):
    """Store given Numpy array in Redis under key name"""
    encoded = array.tobytes()
    red.set(name, encoded)  # Store encoded data in Redis
    return


def load_numpy_from_redis(red, name, dtype=np.uint8):
    """Retrieve Numpy array from Redis key name"""
    encoded = red.get(name)
    hwc_offset = 4 * 4
    d, h, w, c = struct.unpack('>IIII', encoded[:hwc_offset])
    array = np.frombuffer(encoded, dtype=dtype, offset=hwc_offset).reshape(d, h, w, c)
    return array


def save_stack_to_redis(red, data, name):
    """Data is dict including timestamp e.g {"stack": stack_in_numpy_array, "timestamp": timestamp}
    """
    array = data["stack"]
    h, w, c, d = array.shape
    shape = struct.pack('>IIII', h, w, c, d)
    encoded = shape + array.tobytes()
    timestamp = data["timestamp"]
    encoded_dict = {"stack": encoded, "timestamp": timestamp}
    red.hmset(name, encoded_dict)
    return


def load_stack_from_redis(red, name, dtype=np.uint8):
    """Retrieve Stack and timestamp from Redis key name"""
    redis_encoded_dict = red.hgetall(name)
    if redis_encoded_dict:
        encoded = redis_encoded_dict[b"stack"]
        hwc_offset = 4 * 4
        d, h, w, c = struct.unpack('>IIII', encoded[:hwc_offset])
        print("d {} h {} w {} c {}".format(d, h, w, c))
        array = np.frombuffer(encoded, dtype=dtype, offset=hwc_offset).reshape(d, h, w, c)
        timestamp = float(redis_encoded_dict[b"timestamp"].decode("utf=8"))
        return {"stack": array, "timestamp": timestamp}
    else:
        return {}


def save_frame_to_redis(red, data, name):
    """Data is dict including timestamp e.g {"frame": encoded_frame, "timestamp": timestamp}
    """
    encoded_frame = data["frame"]
    timestamp = data["timestamp"]
    encoded_dict = {"frame": encoded_frame, "timestamp": timestamp}
    red.hmset(name, encoded_dict)
    return


def set_key(red,data):
    red.mset({cf.FLAG_REDIS_KEY:data})
    return


def load_frame_from_redis(red, name):
    """Retrieve frame and timestamp from Redis key name"""
    redis_encoded_dict = red.hgetall(name)
    if redis_encoded_dict:
        encoded_frame = redis_encoded_dict[b"frame"]
        timestamp = float(redis_encoded_dict[b"timestamp"].decode("utf=8"))
        return {"frame": encoded_frame, "timestamp": timestamp}
    else:
        return {}


def stack_frames(frames):
    """Convert to gray frame and create stack"""
    # TODO: get only red channel is ok??? in case color camera
    assert len(frames) == 5
    frame = np.stack(frames)
    return frame


def find_center(box1, box2):
    """Find center point of box"""
    return [(box1[0] + box2[0]) / 2, (box1[1] + box2[1]) / 2]


def extrapolation_box(first_boxes, first_timestamp, second_boxes, second_timestamp, third_timestamp):
    """Extrapolation box by timestamp"""
    if first_boxes is None or second_boxes is None:
        return []
    # find center point of first box
    first_center = find_center([first_boxes[0][0], first_boxes[0][1]], [first_boxes[0][2], first_boxes[0][3]])
    # find center point of second box
    second_center = find_center([second_boxes[0][0], second_boxes[0][1]], [second_boxes[0][2], second_boxes[0][3]])
    # find ratio: A, B, C => CA/BA
    k = (third_timestamp - first_timestamp) / (second_timestamp - first_timestamp)
    if third_timestamp - second_timestamp > 0.1:
        return []
    # find vector CA
    vector13 = [(second_center[0] - first_center[0]) * k, (second_center[1] - first_center[1]) * k]
    # find center point of new box: vectorCA + first_box
    third_center = [vector13[0] + first_center[0], vector13[1] + first_center[1]]

    corner = [second_boxes[0][2], second_boxes[0][1]]  # Find top_right point of second_box
    length = corner[0] - second_boxes[0][0]  # Length of second_box
    width = second_boxes[0][3] - corner[1]  # Width of second_box
    # find new box after extrapolation
    third_boxes = [
        [third_center[0] - length, third_center[1] - width, third_center[0] + length, third_center[1] + width]]
    # return third_boxes
    return second_boxes

