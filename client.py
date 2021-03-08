#!/usr/bin/env python3
import socket, sys, re
from logger import Logger
from socket_ctx import open_socket
from sefinalum import Sefinalum, frame, end

server_host = '127.0.0.1'
server_port = int(sys.argv[1])

log = Logger(4)

def run():
    with open_socket(server_host, server_port) as sock:
        
        with open(sys.argv[2], 'rb') as f:
            send(f.read(), sock)


def send(msg, sock):
    data = f'bin {len(msg)};'.encode() + msg + end()
        
    while len(data):
        sent = sock.send(data)
        log.info('SEND', f'BYTES: <{sent}>')
        data = data[sent:]

if __name__ == '__main__':
    run()
