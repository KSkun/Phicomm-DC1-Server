import socket
import time
from typing import Dict

from device import PhiCommDC1

devices: Dict[str, PhiCommDC1] = {}


def server_daemon():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 8000))
    sock.listen(5)

    while True:
        sock_a, addr = sock.accept()
        dev = PhiCommDC1(sock_a)
        devices[dev.get_device_info()[2]] = dev


def server_heartbeat():
    while True:
        time.sleep(30)
        for dev in devices.values():
            dev.heartbeat()
