import asyncio
import time

class Clock:
    __tbegin = 0
    l_intv = 0.1

    @classmethod
    def start(cls):
        if cls.__tbegin > 0:
            raise Exception("Clock has already been started")
        cls.__tbegin = time.time()

    @classmethod
    def elapsed(cls, offset = 1):
        return round(time.time() - cls.__tbegin, offset)

    @classmethod
    def elapsed_since(cls, ref_time, offset = 1):
        return round(time.time() - ref_time, offset)

def clock_sync_loop(interval = -1):
    def decorator(func):
        nonlocal interval
        if interval < 0:
            interval = Clock.l_intv

        async def wrapper(self, *args, **kwargs):
            while True:
                await asyncio.sleep(interval)
                await func(self, *args, **kwargs)
        return wrapper
    return decorator
