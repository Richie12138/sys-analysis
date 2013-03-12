# types of events
SNAKE_DIE = "snake-die"
HIGH_SCORE = "high-score"
# etc ..

# mapping
link_dict = {}

def bound(evt, callback):
    # the mapping should finally look like:
    # evt -> [callback1, callback2, ...]
    #
    # a callback currently takes `world` as its parameter.
    pass

class Event:
    def __init__(self, target, evt_type):
        this.target = target
        this.evt_type = evt_types
