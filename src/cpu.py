import asyncio
import time
from .clock import Clock

class CPU(Clock):
    sw_time = 0.1

    def __init__(self, rq, overhead = False):
        self.job = None
        self.rq = rq
        self._interrupted = False
        self.overhead = overhead

    def interrupt(self):
        self._interrupted = True

    async def set_proc_time(self, quantum = None):
        await asyncio.sleep(quantum or self.job.remaining)
        self.interrupt()


    def is_idle(self):
        return bool(self.job is None)

    async def alloc(self, job):
        if not self.is_idle():
            raise ValueError("CPU is already busy")
        if self.overhead:
            await asyncio.sleep(CPU.sw_time)
        self.job = job
        print(f"Allocated \"{self.job.name}\" [{self.elapsed()}]")

    async def dealloc(self):
        if self.is_idle():
            raise ValueError("CPU is already idle")
        if self.overhead:
            await asyncio.sleep(CPU.sw_time)
        if round(self.job.remaining, 2) > 0:
            await self.rq.enqueue(self.job)
        print(f"Deallocated \"{self.job.name}\" [{self.elapsed()}]")
        self.job = None

    async def execute(self):
        while True:
            await asyncio.sleep(0)
            if self._interrupted:
                raise TimeoutError()

    async def run(self, quantum = None):
        while True:
            await asyncio.sleep(0)
            if self.is_idle():
                continue
            start_time = time.time()

            try:
                await asyncio.gather(
                    self.execute(),
                    self.set_proc_time(quantum)
                )
            except TimeoutError:
                self._interrupted = False
            
            duration = time.time() - start_time
            self.job.remaining -= duration
            await self.dealloc()
