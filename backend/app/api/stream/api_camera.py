from flask import Blueprint, request
import subprocess
import os
from subprocess import Popen
from app.config import DroneDetectionConfig as cf
import time
import logging
from app.extensions import red,set_key

logging.basicConfig(format=cf.LOGGING_FORMAT, datefmt=cf.LOGGING_DATEFMT, level=cf.LOGGING_LEVEL)

api = Blueprint('connection_api', __name__)
RUN_RTSP_DAEMON_PROCESS = None


def _run_daemon(command, env):
    global RUN_RTSP_DAEMON_PROCESS
    RUN_RTSP_DAEMON_PROCESS = Popen(command, env=env)


def _stop_rtsp_daemon():
    global RUN_RTSP_DAEMON_PROCESS
    RUN_RTSP_DAEMON_PROCESS.kill()
    time.sleep(1)
    RUN_RTSP_DAEMON_PROCESS = None


def _is_rtsp_daemon_running():
    global RUN_RTSP_DAEMON_PROCESS
    if RUN_RTSP_DAEMON_PROCESS is not None:
        return True
    else:
        return False


def _form_rtsp_link(params):
    if params["username"] == "" or params['password'] == "":
        return params["rtsp_link"]
    else:
        return "rtsp://" + params["username"] + ":" + params["password"] + "@" + \
               params["rtsp_link"][7:len(params["rtsp_link"])]


@api.route('/connect', methods=['GET'])
def check_connect():
    global RUN_RTSP_DAEMON_PROCESS
    response_fail = {
        'status': False,
        'msg': "Connect to rtsp link fail"
    }
    response_true = {
        'status': True,
        'msg': "Connect to rtsp link successfully"
    }
    params = {
        "rtsp_link": request.args.get('rtsp_link'),
        "username": request.args.get('username'),
        "password": request.args.get('password'),
        "protocol_id": int(request.args.get('selectedProtocol'))
    }
    if not _is_rtsp_daemon_running():
        try:
            my_env = os.environ.copy()
            my_env['PYTHONPATH'] ="/home/bigdata/Documents/backend/"
            protocol_id = params["protocol_id"]
            if protocol_id == 1:  # RTSP/TCP
                link = _form_rtsp_link(params)
                logging.info("Connect to RTSP/TCP camera at {}".format(link))
                my_env.pop('OPENCV_FFMPEG_CAPTURE_OPTIONS', None)
                print("Load rtsp daemon")
                compeleted_process = subprocess.run(['python', 'app/api/stream/rtsp_tcp_daemon.py', '--link', link, '--mode', '1'],env=my_env         )
                if compeleted_process.returncode:
                    logging.info("FAIL to connect to RTSP/TCP camera at {}".format(link))
                    return response_fail, 400
                _run_daemon(['python', 'app/api/stream/rtsp_tcp_daemon.py', '--link', link, '--mode', '0'], my_env)

            elif protocol_id == 3:  # RTSP/UDP
                link = _form_rtsp_link(params)
                logging.info("Connect to RTSP/UDP camera at {}".format(link))
                my_env["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
                compeleted_process = subprocess.run(['python', 'rtsp_udp_daemon.py', '--link', link, '--mode', '1'],
                                                    env=my_env)
                if compeleted_process.returncode:
                    logging.info("FAIL to connect to RTSP/UDP camera at {}".format(link))
                    return response_fail, 400
                _run_daemon(['python', 'rtsp_udp_daemon.py', '--link', link, '--mode', '0'], my_env)

            elif protocol_id == 4:  # RTP/MPEGTS
                link = _form_rtsp_link(params)
                logging.debug("Connect to RTP/MPEGTS camera at {}".format(link))
                my_env.pop('OPENCV_FFMPEG_CAPTURE_OPTIONS', None)
                compeleted_process = subprocess.run(['python', 'rtp_mpegts_daemon.py', '--link', link, '--mode', '1'],
                                                    env=my_env)
                if compeleted_process.returncode:
                    logging.info("FAIL to connect to RTP/MPEGTS camera at {}".format(link))
                    return response_fail, 400
                _run_daemon(['python', 'rtp_mpegts_daemon.py', '--link', link, '--mode', '0'], my_env)

            elif protocol_id == 2:  # RTP/SDP
                SDP_FILENAME = "rtp.sdp"
                sdp_content = params["rtsp_link"]
                logging.info("Connect to RTP/SDP camera using: \n {}".format(sdp_content))
                with open(SDP_FILENAME, "w") as text_file:
                    text_file.write(sdp_content)
                # WARNING: current ffmpeg version have bug with rtp_mpegts which has just fixed for ffmpeg
                # but not for one in opencv yet. Just wait until next version opencv or see below
                # https://answers.opencv.org/question/124858/how-to-build-opencv_ffmpegdll-from-patched-ffmpeg-source/
                my_env["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "protocol_whitelist;file,rtp,udp,tcp"
                compeleted_process = subprocess.run(
                    ['python', 'rtp_sdp_daemon.py', '--filename', SDP_FILENAME, '--mode', '1'], env=my_env)
                if compeleted_process.returncode:
                    logging.info("FAIL to connect to RTP/SDP camera using: \n {}".format(sdp_content))
                    return response_fail, 400
                _run_daemon(['python', 'rtp_sdp_daemon.py', '--filename', SDP_FILENAME, '--mode', '0'], my_env)
            else:
                logging.info("FAIL Not supported protocol")
                return response_fail, 400
            return response_true, 200
        except Exception as e:
            logging.exception("Neglect connection.")
            return response_fail, 400
    logging.info("FAIL to connect because another camera connection existed, please disconnect it and retry.")
    return response_fail, 400


@api.route('/disconnect', methods=['GET'])
def disconnect():
    response_true = {
        'status': True,
        'msg': "Disconnect rtsp link successfully"
    }
    logging.info("Disconnect to camera.")
    if RUN_RTSP_DAEMON_PROCESS is not None:
        _stop_rtsp_daemon()
    return response_true, 200


@api.route('/begin_train',methods=['GET'])
def begin_train():
    set_key(red,data="TRAIN")


@api.route('/train_new',methods=['POST'])
def train_new():
    return True