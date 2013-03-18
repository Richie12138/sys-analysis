from __future__ import print_function
import inspect

LOG_FILE = 'debug.log'
_logFile = open(LOG_FILE, 'w')

def dprint(*args, **kwargs):
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    print('[{}]: '.format(module.__name__), *args)
    print('[{}]: '.format(module.__name__), *args, file=_logFile)
