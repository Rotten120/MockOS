from uuid import uuid4
from enum import Enum

class Status(Enum):
    NEW = 0
    READY = 1
    RUNNING = 2
    WAITING = 3
    TERMINATED = 4

class Process:
    def __init__(self, name, burst = 0.5, arrival = 0, prio = 1):
        self.id = uuid4().int
        self.name = name
        self.status = Status.NEW 

        self.burst = burst
        self.arrival = arrival

        self.remaining = burst
        self.prio = prio
        self.order = None
