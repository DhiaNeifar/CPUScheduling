import numpy as np
from utils import ColorText


class Scheduler(object):
    def __init__(self, Queue, name):
        self.name = name
        self.Queue = Queue
        self.AverageTurnAroundTime = 0
        self.AverageWaitingTime = 0
        self.CPUUtilization = 0
        self.AverageResponseTime = 0

    def schedule(self):
        pass

    def ComputeSchedulerMetrics(self):
        NumberProcesses = len(self.Queue)
        FirstArrival = np.inf
        LatestCompletionTime = 0
        for process in self.Queue:
            self.AverageTurnAroundTime += process.TurnAroundTime
            self.AverageWaitingTime += process.WaitingTime
            self.AverageResponseTime += process.ResponseTime
            self.CPUUtilization += process.BurstTime
            FirstArrival = min(FirstArrival, process.ArrivalTime)
            LatestCompletionTime = max(LatestCompletionTime, process.CompletionTime)

        self.AverageTurnAroundTime = round(self.AverageTurnAroundTime / NumberProcesses, 2)
        self.AverageWaitingTime = round(self.AverageWaitingTime / NumberProcesses, 2)
        self.AverageResponseTime = round(self.AverageResponseTime / NumberProcesses, 2)
        self.CPUUtilization = round(self.CPUUtilization / (LatestCompletionTime - FirstArrival) * 100, 2)
        return {"AverageTurnAroundTime": self.AverageTurnAroundTime,
                "AverageWaitingTime": self.AverageWaitingTime,
                "AverageResponseTime": self.AverageResponseTime,
                "CPUUtilization": self.CPUUtilization}

    def __repr__(self):
        ListAttributes = ["AverageTurnAroundTime", "AverageWaitingTime", "CPUUtilization", "AverageResponseTime"]
        attributes = [f"{attr} {value}" for attr, value in self.__dict__.items() if attr in ListAttributes]
        return ColorText('y', f'Scheduler {self.name}\n') + ColorText("g", "\t\t\t\t".join(attributes))
