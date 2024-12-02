from schedulers.scheduler import Scheduler


class FCFS(Scheduler):
    def __init__(self, Queue):
        super().__init__(Queue)

    def SortQueue(self):
        pass


    def schedule(self):
        ExecutionStart = 0
        for process in self.Queue:
            ExecutionStart = max(ExecutionStart, process.ArrivalTime)
            WaitingTime = ExecutionStart - process.ArrivalTime
            CompletionTime = ExecutionStart + process.BurstTime
            TurnAroundTime = CompletionTime - process.ArrivalTime
            process.ComputeMetrics(ExecutionStart, WaitingTime, CompletionTime, TurnAroundTime)
            ExecutionStart = CompletionTime
        pass
