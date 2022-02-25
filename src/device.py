import socket

from protocol import PhiCommDC1Server
from config import C
from common import log


def _status_number_to_tuple(status: int):
    return (
        status % 10 == 1,
        int(status / 10) % 10 == 1,
        int(status / 100) % 10 == 1,
        int(status / 1000) % 10 == 1
    )


def _tuple_to_status_number(tup: tuple):
    return 1 * (tup[0] if 1 else 0) + \
           10 * (tup[1] if 1 else 0) + \
           100 * (tup[2] if 1 else 0) + \
           1000 * (tup[3] if 1 else 0)


class PhiCommDC1:
    _server: PhiCommDC1Server

    _switch: tuple
    _voltage: int
    _current: int
    _power: int

    _name: str = 'DC1'
    _switch_name: tuple = ('Main', '1', '2', '3')

    def __init__(self, sock: socket.socket):
        self._server = PhiCommDC1Server(sock)
        self.update_status()

        mac_addr = self._server.get_mac_addr().lower()
        if mac_addr in C.keys():
            conf = C[mac_addr]
            self._name = conf.name
            self._switch_name = tuple(conf.switch_name)

        log.info('DC1 device ' + self._server.get_mac_addr() + ' connected from ' + self._server.get_ip_addr())

    def update_status(self):
        result = self._server.request_status()
        self._switch = _status_number_to_tuple(result['status'])
        self._voltage = result['V']
        self._current = result['I']
        self._power = result['P']

    def get_device_info(self) -> tuple:
        return self._name, self._server.get_ip_addr(), self._server.get_mac_addr(), self._switch_name

    def get_status(self) -> tuple:
        return self._switch, self._voltage, self._current, self._power

    def switch(self, status: tuple):
        result = self._server.set_status(_tuple_to_status_number(status))
        self._switch = _status_number_to_tuple(result['status'])

    def heartbeat(self):
        self.update_status()

    def to_dict(self):
        return {
            'ip': self._server.get_ip_addr(),
            'mac': self._server.get_mac_addr(),
            'name': self._name,
            'switch_name': self._switch_name,
            'switch': list(self._switch),
            'measure': {
                'voltage': self._voltage,
                'current': self._current,
                'power': self._power
            }
        }
