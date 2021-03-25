# sefinalum.py
#
# author: Nicholas H.R. Sims
#
# description:
# Portmanteau of latin terms se/finalum, roughly meaning
# 'apart/final', the inverse of latin terms proto/col meaning
# 'origin/together'.
#
# implements simple command interpreter and state machine
# for framing network messages. Not very useful elsewhere.

import os
from fsm import FSM
from logger import Logger

class Sefinalum(FSM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        config = [
            ['size', 'write'],
            ['open'],
            ['close'],
        ]
        
        self.config([['parse']] + [sequence + ['parse'] for sequence in config] + [['kill']])

    def parse(self, data, **ctx):
        try:
            idx = data.index(b';')
            tokens = data[:idx].split(b' ')
            header = tokens[0].decode()
            data = data[idx+1:]
            self.log.debug('PARSE HEADER', header)

            ctx = {'data':data,'idx':idx,'tokens':tokens}
            self.update(ctx)
            
            self.shift(header)
        
        except ValueError:
            return True

    def open(self, tokens, pool, lock, **ctx):
        path = tokens[1].decode()
        with lock:
            if path in pool:
                ctx = {'reply':b'locked;'}
                self.update(ctx)
                self.shift()
                return 'reply'
            pool += [path]
        
        fd = os.open(path, os.O_WRONLY | os.O_CREAT, 0o644)
        self.log.info('OPEN FILE', path)
        
        ctx = {'fd':fd,'path':path,'reply':b'ok;'}
        self.update(ctx)

        self.shift()
        return 'reply'
        
    def size(self, idx, tokens, **ctx):
        size = int(tokens[1])
        self.log.debug('SIZE', f'{size}')

        ctx = {'size':size}
        self.update(ctx)
        
        self.shift()

    def write(self, data, size, fd, **ctx):
        shift = False
        if len(data) >= size:
            output = data[:size]
            data = data[size:]
            shift = True
        else:
            size -= len(data)
            output = data
            data = b''
        os.write(fd, output)
            
        ctx = {'data':data,'size':size}
        self.update(ctx)

        if shift:
            self.shift()
        else:
            return True
        
    def close(self, fd, path, pool, lock, **ctx):
        os.close(fd)
        with lock:
            pool.remove(path)
        self.log.info('CLOSE FILE', path)

        self.shift()
        return True

    def kill(self, **ctx):
        return 'kill'

class frame(object):

    @staticmethod
    def open(name):
        return f'open {name};'.encode()
    
    @staticmethod
    def write(msg):
        return f'size {len(msg)};'.encode() + msg

    @staticmethod
    def close():
        return 'close;'.encode()

    def kill():
        return 'kill;'.encode()
