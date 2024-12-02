from process import Process


def GenerateProcesses(NumberProcesses, LambdaArrival, MeanBurst):
    processes = [Process(LambdaArrival, MeanBurst) for _ in range(NumberProcesses)]
    for i in range(NumberProcesses - 1):
        processes[i + 1].AdjustArrivalTime(processes[i])
    return processes


if __name__ == '__main__':
    GenerateProcesses(10, 3, 5)
