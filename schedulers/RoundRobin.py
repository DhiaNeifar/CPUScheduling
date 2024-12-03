from copy import deepcopy
from schedulers.scheduler import Scheduler


class RoundRobin(Scheduler):
    def __init__(self, Queue, TimeQuantum, name='Round Robin'):
        super().__init__(Queue, name)
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
            if process.ExecutionTime is None:
                process.ExecutionTime = ExecutionStart
            process.BurstTime -= TimeSlice
            ExecutionStart += TimeSlice
            while _queue and _queue[0].ArrivalTime <= ExecutionStart:
                new_process = _queue.pop(0)
                self.ready_queue.append(new_process)
            if process.BurstTime > 0:
                self.ready_queue.append(process)
            for _process in self.Queue:
                if _process.PID == process.PID:
                    if process.BurstTime == 0:
                        CompletionTime = ExecutionStart
                        WaitingTime = CompletionTime - _process.ArrivalTime - _process.BurstTime
                        TurnAroundTime = CompletionTime - _process.ArrivalTime
                        _process.ComputeMetrics(process.ExecutionTime, WaitingTime, CompletionTime, TurnAroundTime)
                    break
