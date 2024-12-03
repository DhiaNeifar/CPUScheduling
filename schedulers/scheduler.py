class Scheduler(object):
    def __init__(self, Queue, name):
        self.name = name
        self.Queue = Queue
        self.AverageTurnAroundTime = None
        self.AverageWaitingTime = None
        self.Throughput = None
        self.CPUUtilization = None

    def schedule(self):
        pass

    def ComputeMetrics(self):
        NumberProcesses = len(self.Queue)
        self.AverageTurnAroundTime = round(sum(process.TurnAroundTime for process in self.Queue) / NumberProcesses, 2)
        self.AverageWaitingTime = round(sum(process.WaitingTime for process in self.Queue) / NumberProcesses, 2)
        TotalCompletionTime = sum([process.CompletionTime for process in self.Queue])
        TotalBurstTime = sum([process.BurstTime for process in self.Queue])
        self.Throughput = round(TotalCompletionTime / NumberProcesses, 2)
        self.CPUUtilization = round(TotalBurstTime / NumberProcesses, 2)

    def __repr__(self):
        return f'Scheduler {self.name}\nAverage TurnAround Time = {self.AverageTurnAroundTime}\tAverage WaitingTime = {self.AverageWaitingTime}\tThroughput = {self.Throughput}\tCPU Utilization = {self.CPUUtilization}'
