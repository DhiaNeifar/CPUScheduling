from copy import deepcopy
from schedulers.scheduler import Scheduler


class PreemptivePriority(Scheduler):
    def __init__(self, Queue, name='Preemptive Priority'):
        super().__init__(Queue, name)
        self.ready_queue = []

    def schedule(self):
        ExecutionStart = 0
        _queue = deepcopy(self.Queue)
        self.ready_queue = []
        current_process = None
        while _queue or self.ready_queue or current_process:
            while _queue and _queue[0].ArrivalTime <= ExecutionStart:
                process = _queue.pop(0)
                self.ready_queue.append(process)
            if current_process:
                self.ready_queue.append(current_process)
                current_process = None
            self.ready_queue.sort(key=lambda proc: proc.Priority)

            if self.ready_queue:
                current_process = self.ready_queue.pop(0)
                if current_process.ExecutionTime is None:
                    current_process.ExecutionTime = ExecutionStart
                next_arrival_time = _queue[0].ArrivalTime if _queue else float('inf')
                time_slice = min(current_process.BurstTime, next_arrival_time - ExecutionStart)
                current_process.BurstTime -= time_slice
                ExecutionStart += time_slice
                if current_process.BurstTime == 0:
                    CompletionTime = ExecutionStart
                    for _process in self.Queue:
                        if _process.PID == current_process.PID:
                            WaitingTime = CompletionTime - _process.ArrivalTime - _process.BurstTime
                            TurnAroundTime = CompletionTime - _process.ArrivalTime
                            _process.ComputeMetrics(current_process.ExecutionTime, WaitingTime, CompletionTime, TurnAroundTime)
                            break
                    current_process = None
            else:
                if _queue:
                    ExecutionStart = _queue[0].ArrivalTime
