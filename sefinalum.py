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
            ['bin', 'extract']
        ]
        
        self.config([['start']] + [sequence + ['start'] for sequence in config] + [['end']])

    def start(self, data, end, store, **ctx):
        try:
            idx = data.index(b';')
            tokens = data[:idx].split(b' ')
            command = tokens[0].decode()
            self.log.debug('PARSE COMMAND', command)
            
            self.shift(command)
            
            ctx = {'data': data, 'idx': idx, 'tokens': tokens, 'end': end, 'store': store}
            self.reset(ctx)
            
            return True
        except ValueError:
            return False

    def bin(self, idx, tokens, **ctx):
        size = int(tokens[1])
        idz = size + idx + 1
        self.log.debug('SIZE/FINAL IDX', f'{size} / {idz}')

        self.shift()
        
        ctx = {'size':size,'idz':idz}
        self.update(ctx)
        
        return True

    def extract(self, idx, idz, data, size, store, **ctx):
        if len(data[idx+1:]) >= size:
            msg = data[idx+1:idz]
            data = data[idz:]
            store += [msg]
            self.shift()
            self.update({'data':data, 'store': store, 'msg': msg})
            return True
        return False

    def end(self, end, **ctx):
        return end

def frame(msg):
    return f'bin {len(msg)};'.encode()

def end():
    return 'end;'.encode()
