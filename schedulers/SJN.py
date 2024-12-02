from copy import deepcopy

from schedulers.scheduler import Scheduler


class SJN(Scheduler):
    def __init__(self, Queue):
        super().__init__(Queue)
        self.ready_queue = []

    def schedule(self):
        ExecutionStart = 0
        _queue = deepcopy(self.Queue)
        while _queue or self.ready_queue:
            while _queue and _queue[0].ArrivalTime <= ExecutionStart:
                process = _queue.pop(0)
                self.ready_queue.append(process)
            if not self.ready_queue:
                if _queue:
                    ExecutionStart = _queue[0].ArrivalTime
                continue
            self.ready_queue.sort(key=lambda proc: proc.BurstTime)
            process = self.ready_queue.pop(0)
            for _process in self.Queue:
                if _process.PID == process.PID:
                    _process.ExecutionTime = ExecutionStart
                    WaitingTime = ExecutionStart - _process.ArrivalTime
                    CompletionTime = ExecutionStart + _process.BurstTime
                    TurnAroundTime = CompletionTime - _process.ArrivalTime
                    _process.ComputeMetrics(ExecutionStart, WaitingTime, CompletionTime, TurnAroundTime)
            ExecutionStart += process.BurstTime
        self.Queue.sort(key=lambda proc: proc.ExecutionTime)
