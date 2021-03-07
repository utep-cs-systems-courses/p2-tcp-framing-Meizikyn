#!/usr/bin/env python3
import socket, sys, re    
from sefinalum import Sefinalum
from logger import Logger

log = Logger(4)

def run():
    try:
        source_addr = ''
        source_port = int(sys.argv[1])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((source_addr, source_port))
        sock.listen(1)
        
        conn, addr = sock.accept()
        log.info('SOCK ACCEPT', f'ADDR: <{addr}>')
        
    
        units = []
        fsm = Sefinalum()
    
        data = conn.recv(4).decode()
        fsm.update({'data': data, 'end': 'end', 'cache': units})
        while True:
    
            result = fsm.call()
            data = fsm['data']
            if 'msg' in fsm:
                msg = fsm.pop('msg')
                log.info('SOCK RECEIVE', msg)

            if result == 'end':
                break

            elif result == False:
                data += conn.recv(4).decode()
                fsm.update({'data': data})          
        
        for msg in units:
            while len(msg):
                sent = conn.send(msg.encode())
                msg = msg[sent:]
                
    except KeyboardInterrupt:
        pass
            
    conn.shutdown(socket.SHUT_WR)
    conn.close()

if __name__ == '__main__':
    run()
