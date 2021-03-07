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
            ['size', 'msg']
        ]
        
        self.config([['parse']] + [sequence + ['parse'] for sequence in config] + [['end']])
        
    def parse(self, data, end, **ctx):
        try:
            idx = data.index(';')
            tokens = data[:idx].split(' ')
            command = tokens[0]
            self.log.debug('PARSE COMMAND', command)
            
            self.shift(command)
            
            ctx = {'data': data, 'idx': idx, 'tokens': tokens, 'end': end}
            self.reset(ctx)
            
            return True
        except ValueError:
            return False

    def size(self, idx, tokens, **ctx):
        size = int(tokens[1])
        idz = size + idx + 1
        self.log.debug('SIZE/FINAL IDX', f'{size} / {idz}')

        self.shift('msg')
        
        ctx = {'size':size,'idz':idz}
        self.update(ctx)
        
        return True

    def msg(self, idx, idz, data, size, cache, **ctx):
        if len(data[idx+1:]) >= size:
            msg = data[idx+1:idz]
            data = data[idz:]
            self.shift('parse')
            self.update({'data':data, 'cache': cache + [msg]})
            return True
        return False

    def end(self, end, **ctx):
        return end
