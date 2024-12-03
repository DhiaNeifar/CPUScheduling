from copy import deepcopy
from schedulers.scheduler import Scheduler


class RoundRobin(Scheduler):
    def __init__(self, Queue, TimeQuantum):
        super().__init__(Queue)
        self.TimeQuantum = TimeQuantum
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

            process = self.ready_queue.pop(0)
            TimeSlice = min(self.TimeQuantum, process.BurstTime)
            process.BurstTime -= TimeSlice
            ExecutionStart += TimeSlice

            for _process in self.Queue:
                if _process.PID == process.PID:
                    if process.BurstTime == 0:
                        CompletionTime = ExecutionStart
                        WaitingTime = CompletionTime - _process.ArrivalTime - _process.BurstTime
                        TurnAroundTime = CompletionTime - _process.ArrivalTime
                        _process.ComputeMetrics(ExecutionStart - TimeSlice, WaitingTime, CompletionTime, TurnAroundTime)
                    else:
                        _process.ExecutionTime = ExecutionStart - TimeSlice

            if process.BurstTime > 0:
                self.ready_queue.append(process)

        self.Queue.sort(key=lambda proc: proc.ExecutionTime)
