from copy import deepcopy

from schedulers.scheduler import Scheduler


class LJF(Scheduler):
    def __init__(self, Queue, name='Longest Job First'):
        super().__init__(Queue, name)
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
            self.ready_queue.sort(key=lambda proc: proc.BurstTime, reverse=True)
            process = self.ready_queue.pop(0)
            for _process in self.Queue:
                if _process.PID == process.PID:
                    _process.ExecutionTime = ExecutionStart
                    WaitingTime = ExecutionStart - _process.ArrivalTime
                    CompletionTime = ExecutionStart + _process.BurstTime
                    TurnAroundTime = CompletionTime - _process.ArrivalTime
                    _process.ComputeProcessMetrics(ExecutionStart, WaitingTime, CompletionTime, TurnAroundTime)
            ExecutionStart += process.BurstTime
