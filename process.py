from __init__ import MinimumBurstTime, MinimumPriorityLevel, MaximumPriorityLevel, MinimumPID, MaximumPID
import numpy as np


class Process(object):
    def __init__(self, LambdaArrival, MeanBurst, Sigma):
        self.PID = np.random.randint(MinimumPID, MaximumPID)
        self.ArrivalTime = np.random.poisson(LambdaArrival)
        self.BurstTime = np.maximum(np.round(np.random.normal(MeanBurst, Sigma)), MinimumBurstTime).astype(int)
        self.Priority = np.random.randint(MinimumPriorityLevel, MaximumPriorityLevel)
        self.ExecutionTime = None
        self.CompletionTime = None
        self.TurnAroundTime = None
        self.WaitingTime = None
        self.ResponseTime = None


    def __repr__(self):
        return f'PID = {self.PID}, Arrival = {self.ArrivalTime}, Burst = {self.BurstTime}, Priority = {self.Priority}, Execution = {self.ExecutionTime}, Completion = {self.CompletionTime}, Turnaround = {self.TurnAroundTime}, Waiting = {self.WaitingTime}'

    def AdjustArrivalTime(self, OtherProcess):
        assert isinstance(OtherProcess, Process)
        self.ArrivalTime += OtherProcess.ArrivalTime

    def ComputeMetrics(self, ExecutionStart, WaitingTime, CompletionTime, TurnAroundTime):
        self.ExecutionTime = ExecutionStart
        self.CompletionTime = CompletionTime
        self.TurnAroundTime = TurnAroundTime
        self.WaitingTime = WaitingTime
        self.ResponseTime = self.ExecutionTime - self.ArrivalTime

    @staticmethod
    def GenerateProcesses(NumberProcesses, LambdaArrival, MeanBurst, Sigma):
        processes = [Process(LambdaArrival, MeanBurst, Sigma) for _ in range(NumberProcesses)]
        for i in range(NumberProcesses - 1):
            processes[i + 1].AdjustArrivalTime(processes[i])
        return processes