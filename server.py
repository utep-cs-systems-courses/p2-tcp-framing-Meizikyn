#!/usr/bin/env python3
import socket, sys, re    
from sefinalum import Sefinalum

def run():
    try:
        source_addr = ''
        source_port = int(sys.argv[1])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((source_addr, source_port))
        sock.listen(1)
        
        conn, addr = sock.accept()
        print(f'[==] (ACCEPT) :: ADDR<{addr}>')
        
    
        units = []
        fsm = Sefinalum()
    
        data = conn.recv(4).decode()
        fsm.update({'data': data, 'end': 'end', 'cache': units})
        while True:
    
            result = fsm.call()
            data = fsm['data']
            if 'msg' in fsm:
                msg += fsm['msg']
                print(f'[==] (RECEIVE) :: {msg}')

            if result == 'end':
                break

            elif result == False:
                data += conn.recv(4).decode()
                fsm.update({'data': data})          
        
    
        while len(msg):
            sent = conn.send(msg.encode())
            msg = msg[sent:]
                
    except KeyboardInterrupt:
        pass
            
    conn.shutdown(socket.SHUT_WR)
    conn.close()

def run_old():
    try:
        source_addr = ''
        source_port = int(sys.argv[1])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((source_addr, source_port))
        sock.listen(1)
        
        conn, addr = sock.accept()
        print(f'[==] (ACCEPT) :: ADDR<{addr}>')
        
    
        state = 'get_command'
        units = []
        tmp = ''
    
        while len(data := conn.recv(4).decode()):
            tmp += data
    
            if state == 'get_command':
                try:
                    idx = tmp.index(';')
                    tokens = tmp[:idx].split(' ')
                    command = tokens[0]
                    print(f'COMMAND: <{command}>')
                    if command == 'end':
                        print('end')
                        break
                    size = int(tokens[1])
                    idz = size + idx + 1
                    state = 'get_msg'
                    continue
                except ValueError:
                    continue
    
            if state == 'get_size':
                try: # ^size 11 Hello World
                    size_idx = tmp[cmd_idx+1:].index(' ') + cmd_idx + 1
                    size = int(tmp[cmd_idx+1:size_idx])
                    end_idx = size + size_idx + 1
                    print(f'SIZE: <{size}>')
                    state = 'get_msg'
                    continue
                except ValueError:
                    continue
    
            if state == 'get_msg':
                if len(tmp[idx+1:]) >= size:
                    msg = tmp[idx+1:idz]
                    units += [msg]
                    tmp = tmp[idz:]
                    print(f'Remaining: <{tmp}>')
                    state = 'get_command'
                    print(f'MSG: <{msg}>')
                    continue
                continue
           
        
        print('[==] (RECEIVE) :: {msg}')
    
        while len(msg):
            sent = conn.send(msg.encode())
            msg = msg[sent:]
                
    except KeyboardInterrupt:
        conn.close()
            
    conn.shutdown(socket.SHUT_WR)
    conn.close()

if __name__ == '__main__':
    run()
