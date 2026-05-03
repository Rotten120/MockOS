from .cpu import CPU
from .clock import Clock, clock_sync_loop
import asyncio

# I MIGHT NEED TO CREATE MY OWN READYQUEUE HERE
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

class CPUScheduler:
    def __init__(self, cpu, rq):
        self.cpu = cpu
        self.rq = rq

    async def get_prio(self, i1, i2):
        for n in range(len(i1) - 1):
            if(i1[n] == i2[n]):
                continue
            if(i1[n] > i2[n]):
                return i2
            if(i1[n] < i2[n]):
                return i1
        return i1

    async def run(self, preempt = False):
        if preempt:
            await self.run_pre()
        else:
            await self.run_npre()

    @clock_sync_loop(interval = 0.5)
    async def run_pre(self):
        if not self.cpu.is_idle():
            try:
                item = await self.rq.q.get_nowait()
            except asyncio.QueueEmpty:
                return 

            # COMPARE
            # IF CPU PROC BETTER, CONTINUE
            # IF ITEM PROC BETTER, INTERRUPT AND SWITCH

    @clock_sync_loop(interval = 0)
    async def run_npre(self):
        if self.cpu.is_idle():
            item = await self.rq.get()
            job = item[-1]                
            await self.cpu.alloc(job)
