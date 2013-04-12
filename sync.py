# Author:
# Description:
from debug import dprint
import config

class Lock:
    def __init__(self):
        self.waitingList = []
        self.owner = None
        self._fail = False

    def __repr__(self):
        return "Lock(pos={}, owner={}, waiting={})".format(self.pos, 
                (self.owner.name if hasattr(self.owner, 'name') else self.owner), 
                len(self.waitingList))

    def acquire(self, target, on_succeed, on_fail):
        if config.PRINT_SYNC: dprint("{} acquire for {}".format(target, self))
        self.waitingList.append((target, on_succeed, on_fail))

    def release(self, target):
        if config.PRINT_SYNC: dprint("{} release {}".format(target, self))
        if self.owner != target:
            raise Exception("{} is not holding the lock. Onwer: {}".format(target, self.owner))
        self.owner = None

    def update(self):
        """
        @return: True if something updated. False if still blocking.
        """
        if len(self.waitingList) > 1:
            self.fail()
        if self._fail:
            self._fail = False
            dprint(self, 'failed')
            for target, on_succeed, on_fail in self.waitingList:
                if on_fail:
                    on_fail()
            self.waitingList = []
            return True
        if self.owner is None:
            if len(self.waitingList) == 1:
                target, on_succeed, on_fail = self.waitingList.pop()
                if config.PRINT_SYNC: dprint('give', self, 'to', target)
                if on_succeed:
                    on_succeed()
                self.owner = target
                return True
        return False

    def fail(self):
        dprint('mark fail', self)
        self._fail = True
