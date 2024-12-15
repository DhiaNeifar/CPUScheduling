import matplotlib.pyplot as plt
import numpy as np
import os

from utils import GetDataPerLambda


def VisualizeFixedLambda(data, x_axis_, Schedulers, _lambda):
    CurrentPath = os.getcwd()
    FiguresFolderName = "Figures"
    FiguresFolderPath = os.path.join(CurrentPath, FiguresFolderName)
    os.makedirs(FiguresFolderPath, exist_ok=True)
    Metrics = ["Average TurnAround Time", "Average Waiting Time", "Average Response Time", "CPU Utilization"]
    for metric in Metrics:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        y_positions = np.arange(len(Schedulers))
        for idx, Scheduler in enumerate(Schedulers):
            mean = np.array(data["data"][Scheduler][metric.replace(' ', '')]["mean"])
            ax.plot(x_axis_, y_positions[idx] * np.ones_like(x_axis_), mean, label=f"{Scheduler}", linewidth=2)
        ax.set_xlabel("Number Of Processes", fontsize=12, labelpad=10)
        ax.set_ylabel("Schedulers", fontsize=12, labelpad=10)
        ax.set_zlabel(f"{metric}", fontsize=12, labelpad=10)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(loc='upper left', fontsize=15)
        filename = f"Metric_{metric.replace(' ', '')}_lambda_{lambda_}.png"
        fig.tight_layout()
        plt.savefig(os.path.join(FiguresFolderPath, filename), bbox_inches='tight')


if __name__ == "__main__":
    NumberSimulations_, NumberProcesses_, lambda__ = 5, [5, 10, 20, 50] + list(range(100, 1100, 100)), [1, 5, 10, 20]
    for lambda_ in lambda__:
        data_, Schedulers_ = GetDataPerLambda(NumberSimulations_, NumberProcesses_, lambda_)
        VisualizeFixedLambda(data_, NumberProcesses_, Schedulers_, lambda_)
