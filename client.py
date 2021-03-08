#!/usr/bin/env python3
import socket, sys, re
from logger import Logger
from socket_ctx import open_socket
from sefinalum import Sefinalum, frame, end

server_host = '127.0.0.1'
server_port = int(sys.argv[1])

def run():
    with open_socket(server_host, server_port) as sock:
        
        msg = sys.argv[2]
        send(msg, sock)


def send(msg, sock):
    data = f'bin {len(msg)};' + msg + end().decode()
        
    while len(data):
        sent = sock.send(data.encode())
        data = data[sent:]

if __name__ == '__main__':
    run()
