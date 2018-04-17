import socket

from datetime import datetime
from concurrent import futures


def blocking_way():
    sock = socket.socket()
    sock.connect(('jd.com', 80))
    request = 'GET / HTTP/1.0\r\nHost: jd.com\r\n\r\n'
    sock.send(request.encode('ascii'))
    response = b''
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        chunk = sock.recv(4096)
    return response

def sync_way():
    res = []
    for i in range(20):
        res.append(blocking_way())

def process_way():
    workers = 10
    with futures.ProcessPoolExecutor(workers) as executor:
        futs = {executor.submit(blocking_way) for i in range(20)}
    return len([fut.result() for fut in futs])

def thread_way():
    workers = 20
    with futures.ThreadPoolExecutor(workers) as executor:
        futs = {executor.submit(blocking_way) for i in range(20)}
    return len([fut.result() for fut in futs])
    

def main():
    start = datetime.now()
    sync_way()
    end = datetime.now()
    interval = end - start

    start_process = datetime.now()
    process_way()
    end_process = datetime.now()
    interval_process = end_process - start_process

    start_thread = datetime.now()
    thread_way()
    end_thread = datetime.now()
    interval_thread = end_thread - start_thread

    print(interval, interval_process, interval_thread, end='\n')

if __name__ == '__main__':
    main()


