import json
import socket
import threading
from typing import Any, Dict

import shortuuid

from common import log


class PhiCommDC1Server:
    _sock: socket.socket
    _ip_addr: str
    _mac_addr: str

    _ctx_lock: threading.Lock
    _ctx_uuid: str

    def __init__(self, sock: socket.socket):
        self._sock = sock
        (ip_addr, ip_port) = sock.getpeername()
        self._ip_addr = ip_addr + ':' + str(ip_port)

        activate_param = self.receive_activate()
        self._mac_addr = activate_param['mac'].lower()

        self._ctx_lock = threading.Lock()

    def __del__(self):
        self._sock.close()

    def get_ip_addr(self):
        return self._ip_addr

    def get_mac_addr(self):
        return self._mac_addr

    def get_socket(self):
        return self._sock

    def send_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        payload_b = bytes(json.dumps(payload) + '\n', encoding='utf-8')
        log.debug('send to ' + self._ip_addr + ' with payload ' + str(payload))
        self._sock.send(payload_b)
        response_b = self._sock.recv(1024)
        response = json.loads(response_b)
        log.debug('receive from ' + self._ip_addr + ' with payload ' + str(response))
        if response['uuid'] == self._ctx_uuid and response['status'] == 200:
            return response['result']
        else:
            raise ValueError('unexpected response for status request: %s' % str(response_b, encoding='utf-8'))

    def receive_activate(self):
        response_b = self._sock.recv(1024)
        response = json.loads(response_b)
        log.debug('receive from ' + self._ip_addr + ' with payload ' + str(response))
        return response['params']

    def request_status(self):
        if self._ctx_lock.acquire(timeout=1):
            self._ctx_uuid = shortuuid.uuid()
            payload = {
                'uuid': self._ctx_uuid,
                'action': 'datapoint',
                'params': {},
                'auth': '',
            }
            result = self.send_request(payload)
            self._ctx_lock.release()
            return result
        else:
            raise TimeoutError('timed out when waiting for other contexts to complete')

    def set_status(self, status: int):
        if self._ctx_lock.acquire(timeout=1):
            self._ctx_uuid = shortuuid.uuid()
            payload = {
                'uuid': self._ctx_uuid,
                'action': 'datapoint=',
                'params': {'status': status},
                'auth': '',
            }
            result = self.send_request(payload)
            self._ctx_lock.release()
            return result
        else:
            raise TimeoutError('timed out when waiting for other contexts to complete')
