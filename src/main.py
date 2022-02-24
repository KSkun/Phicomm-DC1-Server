import socket

from device import PhiCommDC1Plug

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 8000))
    sock.listen(5)

    sock_a, addr = sock.accept()
    print(addr)
    sock_a.close()
    sock.close()
