from copy import deepcopy
from schedulers.scheduler import Scheduler


class ShortestRemainingTimeFirst(Scheduler):
    def __init__(self, Queue, name='Shortest Remaining Time First'):
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
            self.ready_queue.sort(key=lambda proc: proc.BurstTime)
            process = self.ready_queue.pop(0)
            if process.ExecutionTime is None:
                process.ExecutionTime = ExecutionStart
            next_arrival_time = _queue[0].ArrivalTime if _queue else float('inf')
            if process.BurstTime + ExecutionStart <= next_arrival_time:
                ExecutionStart += process.BurstTime
                process.BurstTime = 0
                CompletionTime = ExecutionStart
                for _process in self.Queue:
                    if _process.PID == process.PID:
                        WaitingTime = CompletionTime - _process.ArrivalTime - _process.BurstTime
                        TurnAroundTime = CompletionTime - _process.ArrivalTime
                        _process.ComputeProcessMetrics(process.ExecutionTime, WaitingTime, CompletionTime, TurnAroundTime)
                        break
            else:
                time_slice = next_arrival_time - ExecutionStart
                process.BurstTime -= time_slice
                ExecutionStart += time_slice
                self.ready_queue.append(process)
