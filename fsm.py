# fsm.py
#
# author: Nicholas H.R. Sims
#
# description:
# FSM with context swapping support.

from logger import Logger

class FSM(object):
    def __init__(self, auto=False, log_level=0):
        self.auto = auto
        self.table = {}
        self.graph = {}
        self.current = None
        self.context = {}

        self.log = Logger(log_level)

    def __getitem__(self, key):
        return self.context[key]

    def __iter__(self):
        return iter(self.context)

    def pop(self, key):
        return self.context.pop(key)

    def config(self, config):
        for sequence in config:
            multi = len(sequence) > 1
            for idx, state in enumerate(sequence[:-1] if multi else sequence):
                self.add(state, getattr(self, state), sequence[idx+1] if multi else None)
        
    def inject(self, **ctx):
        for k,v in ctx:
            setattr(self, k, v)

    def reset(self, ctx):
        self.context = ctx
        self.log.debug('FSM CTX RESET', ctx)
            
    def update(self, ctx):
        self.context.update(ctx)
        self.log.debug('FSM CTX UPDATE', ctx)

    def add(self, name, closure, to=None):
        self.table[name] = closure
        self.current = self.current if self.current else name
        self.graph[name] = to
        self.log.debug('FSM CONFIG', f'FROM: <{name}> TO: <{to}>')

    def call(self, **ctx):
        self.log.debug('FSM CALL', f'FUNC: <{self.current}>')
        self.context.update(ctx)
        rvalue = self.ortho()
        if self.auto:
            self.shift()
        return rvalue

    def ortho(self):
        return self.table[self.current](**self.context)

    def shift(self, to=None):
        if not to and self.graph[self.current]:
            self.log.debug('FSM SHIFT', 'FROM: <{self.current}> TO: <{to}>')
            self.current = self.graph[self.current]
            return
        if to in self.graph:
            self.log.debug('FSM SHIFT', 'FROM: <{self.current}> TO: <{to}>')
            self.current = to
            return
        raise InvalidStateError(f'Shift state not in state table: {to if to else self.graph[self.current]}')
        

class InvalidStateError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
