import _thread
import logging

from flask import Flask

from api import api_bp
from common import log
from config import load_config
from server import server_daemon, server_heartbeat

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    load_config('default.json')
    log.info('config loaded')

    server_thread = _thread.start_new_thread(server_daemon, ())
    heartbeat_thread = _thread.start_new_thread(server_heartbeat, ())

    app = Flask(__name__)
    app.register_blueprint(api_bp)
    app.run(host='0.0.0.0', port=8090)
