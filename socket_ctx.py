#!/usr/bin/env python3

import socket
from logger import Logger

class open_socket(object):
    def __init__(self, server_host, server_port, log_level=2):
        self.sock = None
        self.server_host = server_host
        self.server_port = server_port
        self.log = Logger(log_level)
        
    def __enter__(self):
        for addr_info in socket.getaddrinfo(self.server_host, self.server_port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            addr_family, sock_type, proto, canonical_name, sock_addr = addr_info
            try:
                self.sock = socket.socket(addr_family, sock_type, proto)
                self.log.debug('CREATE SOCKET' f'AF<{addr_family}> TYPE<{sock_type}> PROTOCOL<{proto}>')
            except socket.error as err:
                self.log.error('SOCK CREATE FAILURE', err)
                self.sock = None
                continue
            
            try:
                self.sock.connect(sock_addr)
                self.log.debug('SOCK CONNECT', f'TARGET<{sock_addr}>')
            except socket.error as err:
                self.log.error('SOCK CONNECT FAILURE', err)
                self.sock.close()
                self.sock = None
                continue
        return self

    def send(self, *args, **kwargs):
        return self.sock.send(*args, **kwargs)

    def recv(self, *args, **kwargs):
        return self.sock.recv(*args, **kwargs)

    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.close()
        self.sock = None
