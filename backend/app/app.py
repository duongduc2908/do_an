# -*- coding: utf-8 -*-
import logging
import traceback
from time import strftime
from flask import Flask
from app.api import v1 as api_v1
from app.api import stream as api_stream
from app.extensions import jwt, client, app_log_handler, socketio, load_frame_from_redis, red
from .settings import ProdConfig
from flask import Flask, session, request
from flask_socketio import emit
from flask_cors import CORS

users = {}


def create_app(config_object=ProdConfig, content='app'):
    """
    Init App
    :param config_object:
    :param content:
    :return:
    """
    app = Flask(__name__, static_url_path="", static_folder="./template", template_folder="./template")
    app.config.from_object(config_object)
    register_extensions(app, content, config_object)
    register_blueprints(app)
    CORS(app)
    return app


def register_extensions(app, content, config_object):
    """
    Init extension
    :param app:
    :param content:
    :return:
    """
    client.app = app
    client.init_app(app)
    socketio.init_app(app)
    # don't start extensions if content != app
    if content == 'app':
        jwt.init_app(app)
    # logger
    logger = logging.getLogger('api')
    logger.setLevel(logging.ERROR)
    logger.addHandler(app_log_handler)

    @app.after_request
    def after_request(response):
        # This IF avoids the duplication of registry in the log,
        # since that 500 is already logged via @app.errorhandler.
        if response.status_code != 500:
            ts = strftime('[%Y-%b-%d %H:%M]')
            logger.error('%s %s %s %s %s %s',
                         ts,
                         request.remote_addr,
                         request.method,
                         request.scheme,
                         request.full_path,
                         response.status)
        return response

    @app.errorhandler(Exception)
    def exceptions(e):
        ts = strftime('[%Y-%b-%d %H:%M]')
        tb = traceback.format_exc()
        error = '{} {} {} {} {} 5xx INTERNAL SERVER ERROR\n{}'.format \
                (
                ts,
                request.remote_addr,
                request.method,
                request.scheme,
                request.full_path,
                tb
            )

        logger.error(error)

        return "Internal Server Error", 500


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user = client.db.user.find_one({'_id': identity})
    if user['group_role_id'] == '1':
        return {'is_admin': True, 'is_phuong': False, 'is_benh_vien': False, 'full_name': user['full_name']}
    elif user['group_role_id'] == '2':
        return {'is_admin': False, 'is_phuong': True, 'is_benh_vien': False, 'full_name': user['full_name']}
    else:
        return {'is_admin': False, 'is_phuong': False, 'is_benh_vien': True, 'full_name': user['full_name']}


def register_blueprints(app):
    """
    Init blueprint for api url
    :param app:
    :return:
    """
    app.register_blueprint(api_v1.auth.api, url_prefix='/api/v1/auth')
    app.register_blueprint(api_v1.user.api, url_prefix='/api/v1/user')
    app.register_blueprint(api_v1.hospital.api, url_prefix='/api/v1/hospital')
    app.register_blueprint(api_v1.apartment.api, url_prefix='/api/v1/apartment')
    app.register_blueprint(api_v1.place.api, url_prefix='/api/v1/place')
    app.register_blueprint(api_v1.police.api, url_prefix='/api/v1/police')
    app.register_blueprint(api_v1.history.api, url_prefix='/api/v1/history')
    app.register_blueprint(api_v1.upload_file.api, url_prefix='/api/v1/file')
    app.register_blueprint(api_stream.api_camera.api, url_prefix='/api/stream/connection_api')
    app.register_blueprint(api_v1.import_json.api, url_prefix='/api/v1/import_json')
    app.register_blueprint(api_v1.department.api, url_prefix='/api/v1/department')
    app.register_blueprint(api_v1.employee.api, url_prefix='/api/v1/employee')





@socketio.on('connect')
def connect():
    logging.debug('Client connected {}'.format(request.sid))
    @socketio.on('new_frame_event')
    def send_new_frame(message):
        # global fake_detection
        # Message interface includes three keys: frame, detection, room.
        session['receive_count'] = session.get('receive_count', 0) + 1
        room = message['room']

        detection = message['detection']
        # detection = fake_detection

        frame_key = message['frame']
        frame_dict = load_frame_from_redis(red, frame_key)
        image_data = frame_dict["frame"]

        if room:
            emit('imageConversionByClient', {
                'buffer': image_data,
                'timestamp': detection['timestamp'],
                'boxes': detection['boxes'],
                'scores': detection['scores'],
                'classes': detection['classes']
            }, room=room)

            # logging.info("Emit new frame of timestamp {} to frontends at {}".format(detection['timestamp'], datetime.now().timestamp()))
        else:
            emit('imageConversionByClient', {
                'buffer': image_data,
                'timestamp': detection['timestamp'],
                'boxes': detection['boxes'],
                'scores': detection['scores'],
                'classes': detection['classes']
            }, broadcast=True)

            # logging.info("Emit new frame of timestamp {} to frontends at {}".format(detection['timestamp'], datetime.now().timestamp()))


    @socketio.on('disconnect')
    def disconnect():
        logging.debug('Client disconnected {}'.format(request.sid))
