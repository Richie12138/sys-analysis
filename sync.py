# Author:
# Description:
from debug import dprint

class Lock:
    def __init__(self):
        self.waitingList = []
        self.owner = None

    def __repr__(self):
        return "Lock(pos={}, owner={}, waiting={})".format(self.pos, self.owner, len(self.waitingList))

    def acquire(self, target, on_succeed, on_fail):
        dprint("{} acquire for {}".format(target, self))
        self.waitingList.append((target, on_succeed, on_fail))

    def release(self, target):
        dprint("{} release {}".format(target, self))
        if self.owner != target:
            raise Exception("{} is not holding the lock. Onwer: {}".format(target, self.owner))
        self.owner = None

    def update(self):
        """
        @return: True if something updated. False if still blocking.
        """
        if len(self.waitingList) > 1:
            self.fail()
            return True
        if self.owner is None:
            if len(self.waitingList) == 1:
                target, on_succeed, on_fail = self.waitingList.pop()
                # dprint('give', self, 'to', target)
                if on_succeed:
                    on_succeed()
                self.owner = target
                return True
        return False

    def fail(self):
        # dprint(self, 'failed')
        for target, on_succeed, on_fail in self.waitingList:
            if on_fail:
                on_fail()
        self.waitingList = []
