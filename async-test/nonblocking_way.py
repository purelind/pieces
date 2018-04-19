import socket

from datetime import datetime


def nonblocking_way():
    sock = socket.socket()
    sock.setblocking(False)
    try:
        sock.connect(('jd.com', 80))
    except BlockingIOError:
        pass
    request = 'GET /HTTP/1.0\r\nHost: jd.com\r\n\r\n'
    data = request.encode('ascii')
    while True:
        try:
            sock.send(data)
            break
        except OSError:
            pass

    response = b''
    while True:
        try:
            chunk = sock.recv(4096)
            while chunk:
                response += chunk
                chunk = sock.recv(4096)
            break
        except OSError:
            pass
    return response


def sync_way():
    res = []
    for i in range(10):
        res.append(nonblocking_way())
    return len(res)


def main():
    start_sync = datetime.now()
    sync_way()
    end_sync = datetime.now()
    interval_sync = end_sync - start_sync
    print(interval_sync)

if __name__ == '__main__':
    main()
