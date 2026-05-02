import time

class Clock:
    __tbegin = 0

    @classmethod
    def start(cls):
        if cls.__tbegin > 0:
            raise Exception("Clock has already been started")
        cls.__tbegin = time.time()

    @classmethod
    def elapsed(cls, offset = 2):
        return round(time.time() - cls.__tbegin, 2)
