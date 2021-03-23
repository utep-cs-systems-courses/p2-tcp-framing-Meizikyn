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

from fsm import FSM
from logger import Logger

class Sefinalum(FSM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        config = [
            ['size', 'write']
        ]
        
        self.config([['parse']] + [sequence + ['parse'] for sequence in config] + [['end']])

    def parse(self, data, end, store, **ctx):
        try:
            idx = data.index(b';')
            tokens = data[:idx].split(b' ')
            header = tokens[0].decode()
            self.log.debug('PARSE HEADER', header)
            
            self.shift(header)
            
            ctx = {'data': data, 'idx': idx, 'tokens': tokens, 'end': end, 'store': store}
            self.reset(ctx)
            
            return True
        except ValueError:
            return False

    def size(self, idx, tokens, **ctx):
        size = int(tokens[1])
        idz = size + idx + 1
        self.log.debug('SIZE/FINAL IDX', f'{size} / {idz}')

        self.shift()
        
        ctx = {'size':size,'idz':idz}
        self.update(ctx)
        
        return True

    def write(self, idx, idz, data, size, store, **ctx):
        if len(data[idx+1:]) >= size:
            msg = data[idx+1:idz]
            data = data[idz:]
            store += [msg]
            
            self.shift()
            
            ctx = {'data':data, 'store': store, 'msg': msg}
            self.update(ctx)
            
            return True
        return False

    def close(self, close, **ctx):
        return close

    def end(self, end, **ctx):
        return end

class frame(object):

    @staticmethod
    def open(mode, name):
        return f'open {mode} {name};'.encode()
    
    @staticmethod
    def write(msg):
        return f'size {len(msg)};'.encode() + msg

    @staticmethod
    def close():
        return 'close;'.encode()

    def end():
        return 'end;'.encode()
