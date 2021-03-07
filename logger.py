import os, sys

class Logger(object):
    def __init__(self, level=0):
        self.level = level
        if level < 4:
            self.debug = null

        if level < 3:
            self.info = null

        if level < 2:
            self.warning = null
            
        if level < 1:
            self.error = null

    def null(self, **kwargs):
        pass

    def base(self, event, msg, moniker):
        os.write(2, f'[{moniker*2}] ({event}) :: {msg}\n')
        sys.stderr.flush()

    def debug(self, event, msg):
        self.base(event, msg, '=')
    
    def info(self, event, msg):
        self.base(event, msg, 'I')

    def warning(self, event, msg):
        self.base(event, msg, 'W')

    def error(self, event, msg):
        self.base(event, msg, 'E')
