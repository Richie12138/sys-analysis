from __future__ import print_function
import inspect

LOG_FILE = 'debug.log'
_logFile = open(LOG_FILE, 'w')

def dprint(*args, **kwargs):
    frame = inspect.stack()[1]
    modules = []
    stacks = inspect.stack()[1:]
    for frame in stacks:
        name = inspect.getmodule(frame[0]).__name__
        if name != '__main__':
            modules.append(name)
    if not modules:
        modules.append('__main__')
    modules = '->'.join(x for x in reversed(modules))
    print('[{}]: '.format(modules), *args)
    print('[{}]: '.format(modules), *args, file=_logFile)
