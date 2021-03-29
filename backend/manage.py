from app.app import create_app
from app.extensions import socketio
from app.settings import DevConfig
# call config service
# CONFIG = DevConfig if os.environ.get('FLASK_DEBUG') == '1' else ProdConfig
CONFIG = DevConfig


app = create_app(config_object=CONFIG)

if __name__ == '__main__':
    socketio.run(app,host='localhost', debug=False, port=4321)
    # socketio.run(app, debug=False, port=4321)
    # app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=True)

