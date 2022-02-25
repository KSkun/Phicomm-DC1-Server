import _thread
import logging
import time

from config import load_config
from common import log
from server import server_daemon, server_heartbeat

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    load_config('default.json')
    log.info('config loaded')

    server_thread = _thread.start_new_thread(server_daemon, ())
    heartbeat_thread = _thread.start_new_thread(server_heartbeat, ())

    while True:
        time.sleep(1)
