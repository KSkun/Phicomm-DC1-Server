import collections
import socket

import getmac

PhiCommDC1Plug = collections.namedtuple('PhiCommDC1Plug', ['main', 'plug_1', 'plug_2', 'plug_3'])


class PhiCommDC1:
    """PhiComm DC1 Device Class"""

    _sock: socket.socket
    _ip_addr: str
    _mac_addr: str

    _name: str
    _port: PhiCommDC1Plug
    _voltage: int
    _current: int
    _power: int

    def __init__(self, sock: socket.socket):
        self._sock = sock
        (ipAddr, ipPort) = sock.getpeername()
        self._ipAddr = ipAddr + ':' + ipPort
        self._macAddr = getmac.get_mac_address(ip=ipAddr)

        self._name = 'DC1'

    def update_status(self):
        pass  # TODO
