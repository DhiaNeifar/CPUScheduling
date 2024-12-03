from __init__ import MinimumBurstTime, MinimumPriorityLevel, MaximumPriorityLevel
import numpy as np


class Process(object):
    def __init__(self, LambdaArrival, MeanBurst):
        self.PID = np.random.randint(0, 65335)
        self.ArrivalTime = np.random.poisson(LambdaArrival)
        self.BurstTime = np.maximum(np.round(np.random.exponential(MeanBurst)), MinimumBurstTime).astype(int)
        self.Priority = np.random.randint(MinimumPriorityLevel, MaximumPriorityLevel)
        self.ExecutionTime = None
        self.CompletionTime = None
        self.TurnAroundTime = None
        self.WaitingTime = None


    def __repr__(self):
        return f'PID = {self.PID}, Arrival = {self.ArrivalTime}, Burst = {self.BurstTime}, Priority = {self.Priority}, Execution = {self.ExecutionTime}, Completion = {self.CompletionTime}, Turnaround = {self.TurnAroundTime}, Waiting = {self.WaitingTime}'
        # f'Arrival = {self.ArrivalTime}, Burst = {self.BurstTime}, Execution = {self.ExecutionTime}'

    def AdjustArrivalTime(self, OtherProcess):
        assert isinstance(OtherProcess, Process)
        self.ArrivalTime += OtherProcess.ArrivalTime

    def ComputeMetrics(self, ExecutionStart, WaitingTime, CompletionTime, TurnAroundTime):
        self.ExecutionTime = ExecutionStart
        self.CompletionTime = CompletionTime
        self.TurnAroundTime = TurnAroundTime
        self.WaitingTime = WaitingTime
