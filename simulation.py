from process import Process
from schedulers.FCFS import FirstComeFirstServe
from schedulers.SJN import SJN
from schedulers.LJF import LJF
from schedulers.NonPreemptivePriority import NonPreemptivePriority
from schedulers.PreemptivePriority import PreemptivePriority
from schedulers.RoundRobin import RoundRobin
from schedulers.SRTF import ShortestRemainingTimeFirst
from schedulers.LRBT import LongestRemainingBurstTime
from schedulers.HRRN import HighestResponseRatioNext


def main():
    NumberSimulations = 100
    NumberProcesses = [5, 10, 20, 50] + list(range(100, 1100, 100))
    Lambdas = [1, 5, 10, 20]
    MeanBurst = 10
    Sigma = 7
    for NumberProcess in NumberProcesses:
        for Lambda in Lambdas:
            print('\n' + '#' * 60 + '\n')
            print(f'Number of Processes: {NumberProcess}\tLambda: {Lambda}')
            simulation = 0
            while simulation < NumberSimulations:
                print('-' * 60)
                print(f'Simulation {simulation + 1} out of {NumberSimulations}')
                Simulation(NumberProcess, Lambda, MeanBurst, Sigma)
                simulation += 1
            print('-' * 60)


def Simulation(NumberProcess, Lambda, MeanBurst, Sigma):
    processes = Process.GenerateProcesses(NumberProcess, Lambda, MeanBurst, Sigma)
    Schedulers = [
        FirstComeFirstServe(processes),
        SJN(processes),
        LJF(processes),
        NonPreemptivePriority(processes),
        PreemptivePriority(processes),
        RoundRobin(processes, TimeQuantum=2),
        RoundRobin(processes, TimeQuantum=5),
        RoundRobin(processes, TimeQuantum=10),
        ShortestRemainingTimeFirst(processes),
        LongestRemainingBurstTime(processes),
        HighestResponseRatioNext(processes)
    ]
    for scheduler in Schedulers:
        scheduler.schedule()




if __name__ == '__main__':
    main()
