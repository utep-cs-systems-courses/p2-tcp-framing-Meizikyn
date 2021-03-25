import os, sys

class Logger(object):
    def __init__(self, level=3):
        self.level = level
        if level < 4:
            self.debug = self.null

        if level < 3:
            self.info = self.null

        if level < 2:
            self.warning = self.null
            
        if level < 1:
            self.error = self.null

    def null(self, *args, **kwargs):
        pass

    def base(self, event, msg, moniker):
        os.write(2, f'[{moniker*2}] ({event}) :: {msg}\n'.encode())
        sys.stderr.flush()

    def debug(self, event, msg):
        self.base(event, msg, '=')
    
    def info(self, event, msg):
        self.base(event, msg, 'I')

    def warning(self, event, msg):
        self.base(event, msg, 'W')

    def error(self, event, msg):
        self.base(event, msg, 'E')
