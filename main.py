from src import *
import asyncio

jobs = [
    Process("A", prio = 0, burst = 2, arrival = 1),
    Process("B", prio = 1, burst = 3.5, arrival = 0),
    Process("C", prio = 2, burst = 1, arrival = 4),
    Process("D", prio = 3, burst = 1, arrival = 2),
    Process("E", prio = 4, burst = 3, arrival = 1)
]

# Quantum and preempt cannot have a non-None val
# and True value simultaneously, respectively

async def main():
    rqueue = ReadyQueue(algo = 1)

    cpu = CPU(rqueue, overhead = False)
    csched = CPUScheduler(cpu, rqueue)
    jsched = JobScheduler(jobs, rqueue)
  
    Clock.start()
    await asyncio.gather(
        cpu.run(quantum = None),
        csched.run(preempt = True),
        jsched.start()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Done")
