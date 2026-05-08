from .clock import Clock
import asyncio
import itertools

class JobScheduler:
    counter = itertools.count()
    def __init__(self, jobs, rq):    
        self._tjobs = sorted(jobs, key = lambda j: j.arrival)
        self.job_queue = []
        self.rq = rq

    async def start(self):
        await asyncio.gather(*[self.load(job, True) for job in self._tjobs])

    async def load(self, job, init_load = False):
        if init_load:
            await asyncio.sleep(job.arrival)
        else:
            job.arrival = Clock.elapsed()

        order = next(JobScheduler.counter)
        job.order = order

        await self.rq.enqueue(job)
        print(f"  Loaded \"{job.name}\" [{Clock.elapsed()}]")
