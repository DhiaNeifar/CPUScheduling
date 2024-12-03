from copy import deepcopy
from schedulers.scheduler import Scheduler


class HighestResponseRatioNext(Scheduler):
    def __init__(self, Queue, name='Highest Response Ratio Next'):
        super().__init__(Queue, name)
        self.ready_queue = []

    def schedule(self):
        ExecutionStart = 0
        _queue = deepcopy(self.Queue)
        self.ready_queue = []

        while _queue or self.ready_queue:
            while _queue and _queue[0].ArrivalTime <= ExecutionStart:
                process = _queue.pop(0)
                self.ready_queue.append(process)

            if not self.ready_queue:
                if _queue:
                    ExecutionStart = _queue[0].ArrivalTime
                continue

            for process in self.ready_queue:
                waiting_time = ExecutionStart - process.ArrivalTime
                process.ResponseRatio = (waiting_time + process.BurstTime) / process.BurstTime

            self.ready_queue.sort(key=lambda proc: proc.ResponseRatio, reverse=True)
            process = self.ready_queue.pop(0)

            if process.ExecutionTime is None:
                process.ExecutionTime = ExecutionStart

            CompletionTime = ExecutionStart + process.BurstTime
            WaitingTime = CompletionTime - process.ArrivalTime - process.BurstTime
            TurnAroundTime = CompletionTime - process.ArrivalTime

            for _process in self.Queue:
                if _process.PID == process.PID:
                    _process.ComputeMetrics(process.ExecutionTime, WaitingTime, CompletionTime, TurnAroundTime)
                    break

            ExecutionStart = CompletionTime

        self.Queue.sort(key=lambda proc: proc.ExecutionTime)
