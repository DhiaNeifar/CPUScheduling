import numpy as np
import pandas as pd

# Generate processes with ArrivalTime, BurstTime, and Priority

def fcfs_scheduler(processes):
    current_time = 0
    metrics = []

    for _, process in processes.iterrows():
        start_time = max(current_time, process['ArrivalTime'])
        finish_time = start_time + process['BurstTime']
        turnaround_time = finish_time - process['ArrivalTime']
        waiting_time = turnaround_time - process['BurstTime']
        metrics.append({
            'ProcessID': process['ProcessID'],
            'StartTime': start_time,
            'FinishTime': finish_time,
            'TurnaroundTime': turnaround_time,
            'WaitingTime': waiting_time
        })
        current_time = finish_time

    return pd.DataFrame(metrics)


def sjn_scheduler(processes):
    current_time = 0
    ready_queue = []
    metrics = []

    while not processes.empty or ready_queue:
        # Add processes to the ready queue that have arrived by the current time
        ready_queue.extend(processes[processes['ArrivalTime'] <= current_time].to_dict('records'))
        processes = processes[processes['ArrivalTime'] > current_time].reset_index(drop=True)

        if ready_queue:
            # Pick the process with the shortest burst time
            ready_queue.sort(key=lambda x: x['BurstTime'])  # Sort dynamically by BurstTime
            process = ready_queue.pop(0)
            start_time = max(current_time, process['ArrivalTime'])
            finish_time = start_time + process['BurstTime']
            turnaround_time = finish_time - process['ArrivalTime']
            waiting_time = turnaround_time - process['BurstTime']
            metrics.append({'ProcessID': process['ProcessID'], 'StartTime': start_time, 'FinishTime': finish_time,
                'TurnaroundTime': turnaround_time, 'WaitingTime': waiting_time})
            current_time = finish_time
        else:
            # If no process is ready, advance time
            current_time = processes['ArrivalTime'].min()

    return pd.DataFrame(metrics)


def ljf_scheduler(processes):
    current_time = 0
    ready_queue = []
    metrics = []

    while not processes.empty or ready_queue:
        # Add processes to the ready queue that have arrived by the current time
        ready_queue.extend(processes[processes['ArrivalTime'] <= current_time].to_dict('records'))
        processes = processes[processes['ArrivalTime'] > current_time].reset_index(drop=True)

        if ready_queue:
            # Pick the process with the longest burst time
            ready_queue.sort(key=lambda x: -x['BurstTime'])  # Sort descending by BurstTime
            process = ready_queue.pop(0)
            start_time = max(current_time, process['ArrivalTime'])
            finish_time = start_time + process['BurstTime']
            turnaround_time = finish_time - process['ArrivalTime']
            waiting_time = turnaround_time - process['BurstTime']
            metrics.append({
                'ProcessID': process['ProcessID'],
                'StartTime': start_time,
                'FinishTime': finish_time,
                'TurnaroundTime': turnaround_time,
                'WaitingTime': waiting_time
            })
            current_time = finish_time
        else:
            # If no process is ready, advance time
            current_time = processes['ArrivalTime'].min()

    return pd.DataFrame(metrics)


def generate_processes(num_processes, lambda_arrival, mean_burst):
    inter_arrival_times = np.random.poisson(lambda_arrival, size=num_processes)
    arrival_times = np.cumsum(inter_arrival_times)  # Cumulative arrival times
    burst_times = np.maximum(np.round(np.random.exponential(mean_burst, size=num_processes)), 1).astype(int)  # Ensure burst times >= 1
    priorities = np.random.randint(1, 10, size=num_processes)  # Random priorities between 1 and 9
    process_ids = np.arange(1, num_processes + 1)  # Process IDs
    return pd.DataFrame({
        'ProcessID': process_ids,
        'ArrivalTime': arrival_times.astype(int),
        'BurstTime': burst_times.astype(int),
        'Priority': priorities
    })

# Priority Scheduling Algorithm
def priority_scheduler(processes):
    current_time = 0
    ready_queue = []
    metrics = []

    while not processes.empty or ready_queue:
        # Add processes to the ready queue that have arrived by the current time
        ready_queue.extend(processes[processes['ArrivalTime'] <= current_time].to_dict('records'))
        processes = processes[processes['ArrivalTime'] > current_time].reset_index(drop=True)

        if ready_queue:
            # Pick the process with the highest priority (lowest priority value)
            ready_queue.sort(key=lambda x: x['Priority'])  # Sort by priority (ascending)
            process = ready_queue.pop(0)
            start_time = max(current_time, process['ArrivalTime'])
            finish_time = start_time + process['BurstTime']
            turnaround_time = finish_time - process['ArrivalTime']
            waiting_time = turnaround_time - process['BurstTime']
            metrics.append({
                'ProcessID': process['ProcessID'],
                'StartTime': start_time,
                'FinishTime': finish_time,
                'TurnaroundTime': turnaround_time,
                'WaitingTime': waiting_time,
                'Priority': process['Priority']
            })
            current_time = finish_time
        else:
            # If no process is ready, advance time
            current_time = processes['ArrivalTime'].min()

    return pd.DataFrame(metrics)

def round_robin_scheduler(processes, time_quantum):
    current_time = 0
    ready_queue = []
    metrics = []
    remaining_burst = processes.set_index('ProcessID')['BurstTime'].to_dict()  # Track remaining burst time by ProcessID

    while not processes.empty or ready_queue:
        # Add processes to the ready queue that have arrived by the current time
        ready_queue.extend(processes[processes['ArrivalTime'] <= current_time].to_dict('records'))
        processes = processes[processes['ArrivalTime'] > current_time].reset_index(drop=True)

        if ready_queue:
            # Pick the first process in the ready queue
            process = ready_queue.pop(0)
            process_id = process['ProcessID']

            # Calculate execution time for this process
            execution_time = min(remaining_burst[process_id], time_quantum)
            start_time = current_time
            current_time += execution_time
            remaining_burst[process_id] -= execution_time

            # If the process finishes, calculate its metrics
            if remaining_burst[process_id] == 0:
                finish_time = current_time
                turnaround_time = finish_time - process['ArrivalTime']
                waiting_time = turnaround_time - process['BurstTime']
                metrics.append({
                    'ProcessID': process_id,
                    'StartTime': start_time,
                    'FinishTime': finish_time,
                    'TurnaroundTime': turnaround_time,
                    'WaitingTime': waiting_time
                })
            else:
                # If not finished, add it back to the queue
                ready_queue.append(process)
        else:
            # If no process is ready, advance time
            current_time = processes['ArrivalTime'].min()

    return pd.DataFrame(metrics)

def srtf_scheduler(processes):
    current_time = 0
    ready_queue = []
    metrics = []
    remaining_burst = processes.set_index('ProcessID')['BurstTime'].to_dict()  # Track remaining burst time by ProcessID

    while not processes.empty or ready_queue:
        # Add processes to the ready queue that have arrived by the current time
        ready_queue.extend(processes[processes['ArrivalTime'] <= current_time].to_dict('records'))
        processes = processes[processes['ArrivalTime'] > current_time].reset_index(drop=True)

        if ready_queue:
            # Select the process with the shortest remaining time
            ready_queue.sort(key=lambda x: remaining_burst[x['ProcessID']])  # Sort by remaining burst time
            process = ready_queue.pop(0)
            process_id = process['ProcessID']

            # Execute the process for one time unit
            execution_time = 1
            start_time = current_time
            current_time += execution_time
            remaining_burst[process_id] -= execution_time

            # If the process finishes, calculate its metrics
            if remaining_burst[process_id] == 0:
                finish_time = current_time
                turnaround_time = finish_time - process['ArrivalTime']
                waiting_time = turnaround_time - process['BurstTime']
                metrics.append({
                    'ProcessID': process_id,
                    'StartTime': start_time,
                    'FinishTime': finish_time,
                    'TurnaroundTime': turnaround_time,
                    'WaitingTime': waiting_time
                })
            else:
                # If not finished, add it back to the queue
                ready_queue.append(process)
        else:
            # If no process is ready, advance time
            current_time = processes['ArrivalTime'].min()

    return pd.DataFrame(metrics)

def hrrn_scheduler(processes):
    current_time = 0
    ready_queue = []
    metrics = []

    while not processes.empty or ready_queue:
        # Add processes to the ready queue that have arrived by the current time
        ready_queue.extend(processes[processes['ArrivalTime'] <= current_time].to_dict('records'))
        processes = processes[processes['ArrivalTime'] > current_time].reset_index(drop=True)

        if ready_queue:
            # Calculate the Response Ratio for each process
            for process in ready_queue:
                process['ResponseRatio'] = (
                    (current_time - process['ArrivalTime'] + process['BurstTime']) / process['BurstTime']
                )

            # Select the process with the highest response ratio
            ready_queue.sort(key=lambda x: -x['ResponseRatio'])  # Sort descending by Response Ratio
            process = ready_queue.pop(0)
            process_id = process['ProcessID']

            # Execute the selected process to completion
            start_time = max(current_time, process['ArrivalTime'])
            finish_time = start_time + process['BurstTime']
            turnaround_time = finish_time - process['ArrivalTime']
            waiting_time = turnaround_time - process['BurstTime']
            metrics.append({
                'ProcessID': process_id,
                'StartTime': start_time,
                'FinishTime': finish_time,
                'TurnaroundTime': turnaround_time,
                'WaitingTime': waiting_time,
                'ResponseRatio': process['ResponseRatio']
            })
            current_time = finish_time
        else:
            # If no process is ready, advance time
            current_time = processes['ArrivalTime'].min()

    return pd.DataFrame(metrics)

# Example to Test HRRN
np.random.seed(42)
num_processes = 10
lambda_arrival = 3  # Mean arrival rate
mean_burst = 5  # Mean burst time

# Generate Processes
processes = generate_processes(num_processes, lambda_arrival, mean_burst)

# Run HRRN Scheduler
hrrn_results = hrrn_scheduler(processes)

# Display Results
print("Generated Processes:")
print(processes)
print("\nHRRN Scheduling Results:")
print(hrrn_results)
