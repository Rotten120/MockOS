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
        await asyncio.gather(*[self.load(job) for job in self._tjobs])

    async def load(self, job):
        await asyncio.sleep(job.arrival)
        
        order = next(JobScheduler.counter)
        job.order = order

        await self.rq.enqueue(job)
        print(f"Loaded \"{job.name}\" [{Clock.elapsed()}]")

