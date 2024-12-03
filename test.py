import numpy as np

from schedulers.FCFS import FCFS
from schedulers.SJN import SJN
from schedulers.LJF import LJF
from schedulers.Priority import Priority
from schedulers.RoundRobin import RoundRobin
from schedulers.SRTF import ShortestRemainingTimeFirst
from schedulers.LRBT import LongestRemainingBurstTime


from utils import GenerateProcesses


def main():
    NumberProcesses, LambdaArrival, MeanBurst = 10, 3, 5
    Arrivals = [4, 5, 8, 11, 13, 16, 18, 21, 21, 23]
    Burst = [15, 17, 8, 2, 1, 6, 3, 1, 3, 1]
    TimeQuantum = 2
    Priorities = np.random.randint(1, 10, size=NumberProcesses)
    processes = GenerateProcesses(NumberProcesses, LambdaArrival, MeanBurst)
    for index, process in enumerate(processes):
        process.ArrivalTime = Arrivals[index]
        process.BurstTime = Burst[index]
        process.Priority = Priorities[index]

    Scheduler = LongestRemainingBurstTime(processes)
    Scheduler.schedule()
    for index, process in enumerate(processes):
        print(process)
    pass


if __name__ == '__main__':
    main()
