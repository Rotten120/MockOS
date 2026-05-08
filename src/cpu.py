import asyncio
import time
from .clock import Clock, clock_sync_loop

class CPU:
    sw_time = 0.1

    def __init__(self, rq, overhead = False):
        self.job = None
        self.rq = rq
        self.interrupted = False
        self.overhead = overhead

    def interrupt(self):
        self.interrupted = True

    async def set_proc_time(self, quantum = None):
        burst = min(quantum, self.job.remaining) if quantum else self.job.remaining
        await asyncio.sleep(burst)
        self.interrupt()

    def is_idle(self):
        return bool(self.job is None)

    async def alloc(self, job):
        if not self.is_idle():
            raise ValueError("CPU is already busy")
        if self.overhead:
            await asyncio.sleep(CPU.sw_time)

        self.job = job
        self.job.last_cpu_in = time.time()
        self.job.allccnt += 1

        print(f"Allocated \"{self.job.name}\" [{Clock.elapsed()}]")

    async def dealloc(self):
        if self.is_idle():
            raise ValueError("CPU is already idle")
        if self.overhead:
            await asyncio.sleep(CPU.sw_time)

        self.job.last_cpu_out = time.time()

        if self.job.remaining > 0:
            await self.rq.enqueue(self.job)
            print(f" Deallocated \"{self.job.name}\" [{Clock.elapsed()}]")
        else:
            print(f" Remove \"{self.job.name}\" [{Clock.elapsed()}]")
       
        self.job = None

    @clock_sync_loop(interval = 0)
    async def execute(self):
        if self.interrupted:
            raise TimeoutError()
        # Execute Instructions here

    @clock_sync_loop(interval = 0)
    async def run(self, quantum = None):
        if self.is_idle():
            return

        start_time = time.time()
        try:
            t1 = asyncio.create_task(self.execute())
            t2 = asyncio.create_task(self.set_proc_time(quantum))
            group = asyncio.gather(t1, t2)
            await group
        except TimeoutError:
            t1.cancel()
            t2.cancel()
            group.cancel()    

        duration = time.time() - start_time
        self.job.remaining -= round(duration, 2)
        await self.dealloc()
        self.interrupted = False
