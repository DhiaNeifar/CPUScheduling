from schedulers.scheduler import Scheduler


class FirstComeFirstServe(Scheduler):
    def __init__(self, Queue, name='First Come First Serve'):
        super().__init__(Queue, name)

    def SortQueue(self):
        pass


    def schedule(self):
        ExecutionStart = 0
        for process in self.Queue:
            ExecutionStart = max(ExecutionStart, process.ArrivalTime)
            WaitingTime = ExecutionStart - process.ArrivalTime
            CompletionTime = ExecutionStart + process.BurstTime
            TurnAroundTime = CompletionTime - process.ArrivalTime
            process.ComputeProcessMetrics(ExecutionStart, WaitingTime, CompletionTime, TurnAroundTime)
            ExecutionStart = CompletionTime
        pass
