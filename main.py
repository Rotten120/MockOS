from src import *
import asyncio

jobs = [
    Process("A", burst = 2, arrival = 1),
    Process("B", burst = 3.5, arrival = 0),
    Process("C", burst = 1, arrival = 4),
    Process("D", burst = 1, arrival = 2),
    Process("E", burst = 3, arrival = 1)
]

async def main():
    rqueue = ReadyQueue(algo = 1)

    cpu = CPU(rqueue, overhead = False)
    csched = CPUScheduler(cpu, rqueue)
    jsched = JobScheduler(jobs, rqueue)
  
    Clock.start()
    await asyncio.gather(
        cpu.run(),
        csched.run(),
        jsched.start()
    )

if __name__ == "__main__":
    asyncio.run(main())
