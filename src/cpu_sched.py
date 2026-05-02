from .cpu import CPU
from .clock import Clock
import asyncio

class ReadyQueue:
    def __init__(self, algo = 0):
        self.q = asyncio.PriorityQueue()
        self.algo = algo

    async def enqueue(self, order, job):
        if self.algo == 0:
            item = (order, job)
        elif self.algo == 1:
            item = (job.remaining, order, job)
        elif self.algo == 2:
            ITEM = (job.prio, order, job)
        else:
            raise ValueError("Invalid algo code")
        await self.q.put(item)

    async def get(self):
        i_out = await self.q.get()
        return i_out

    async def put(self, item, **kwargs):
        await self.q.put(item, **kwargs)

class CPUScheduler(Clock):
    def __init__(self, cpu, rq):
        self.cpu = cpu
        self.rq = rq

    async def run(self, preempt = False):
        if not preempt:
            while True:
                if self.cpu.is_idle():
                    item = await self.rq.get()
                    job = item[-1]
                    await self.cpu.alloc(job)
                await asyncio.sleep(0)
