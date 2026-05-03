from .cpu import CPU
from .clock import Clock, clock_sync_loop
import asyncio

class ReadyQueue:
    def __init__(self, algo = 0):
        self.q = asyncio.PriorityQueue()
        self.algo = algo

    def normalize(self, job):
        if self.algo == 0:
            return (job.order, job)
        elif self.algo == 1:
            return (job.remaining, job.order, job)
        elif self.algo == 2:
            return (job.prio, job.order, job.name, job)
        raise ValueError("Invalid algo code")

    async def enqueue(self, job):
        item = self.normalize(job)
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

    def get_prio(self, i1, i2):
        for n in range(len(i1) - 1):
            if(i1[n] == i2[n]):
                continue
            if(i1[n] > i2[n]):
                return False
            if(i1[n] < i2[n]):
                return True
        return True

    async def run(self, preempt = False):
        if preempt:
            await self.run_pre()
        else:
            await self.run_npre()

    @clock_sync_loop(interval = 0)
    async def run_pre(self):
        if self.cpu.is_interrupted():
            return

        if not self.cpu.is_idle():
            try:
                qitem = self.rq.q.get_nowait()
            except asyncio.QueueEmpty:
                return
            
            citem = self.rq.normalize(self.cpu.job)
            await self.rq.q.put(qitem)

            if self.get_prio(citem, qitem):
                return
            self.cpu.interrupt()
            return

        if self.cpu.is_idle():
            item = await self.rq.get()
            job = item[-1]
            await self.cpu.alloc(job)
            return

    @clock_sync_loop(interval = 0)
    async def run_npre(self):
        if self.cpu.is_idle():
            item = await self.rq.get()
            job = item[-1]                
            await self.cpu.alloc(job)
