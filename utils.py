import os
import json
import statistics


def ColorText(color, text):
    if color == 'r':
        return f'\033[31m{text}\033[0m'
    if color == 'g':
        return f'\033[32m{text}\033[0m'
    if color == 'y':
        return f'\033[33m{text}\033[0m'
    if color == 'b':
        return f'\033[34m{text}\033[0m'


def InitDisplay():
    InitMessage = """
            ##################################################################################################
            ##                                                                                              ##
            ##                     ####################################################                     ##
            ##                     # DHIA NEIFAR IS THE SOLE PROPRIETARY OF THIS CODE #                     ##
            ##                     ####################################################                     ##
            ##                                                                                              ##
            ##                                                                                              ##
            ##                     ####################################################                     ##
            ##                     # THIS CODE HAS BEEN DEVELOPED FOR ECE 5&* PROJECT #                     ##
            ##                     ####################################################                     ##
            ##                                                                                              ##
            ##################################################################################################"""
    print(ColorText("b", InitMessage))


def SaveData(SimulationID, NumberProcesses, lambda_, data):
    CurrentPath = os.getcwd()
    DataSavingPath = os.path.join(CurrentPath, "Trials")
    os.makedirs(DataSavingPath, exist_ok=True)
    FileName = f"{NumberProcesses}_{lambda_}_{SimulationID}.json"
    FilaPath = os.path.join(DataSavingPath, FileName)
    ToSave = {
        "NumberProcesses": NumberProcesses,
        "Lambda": lambda_,
        "SimulationID": SimulationID,
        "data": data
    }

    with open(FilaPath, "w") as file:
        json.dump(ToSave, file, indent=4)


def GetMeanStd(NumberSimulations, NumberProcess, lambda_):
    CurrentPath = os.getcwd()
    DataPath = os.path.join(CurrentPath, "Trials__")
    simulation = 0
    Data = None
    while simulation < NumberSimulations:
        FileName = f"{NumberProcess}_{lambda_}_{simulation + 1}.json"
        FilaPath = os.path.join(DataPath, FileName)
        with open(FilaPath, "r") as file:
            data = json.load(file)
        if Data is None:
            Data = data
            Data.pop("SimulationID")
            for scheduler in Data["data"].keys():
                for metric, value in Data["data"][scheduler].items():
                    Data["data"][scheduler][metric] = [value]
        else:
            for scheduler in Data["data"].keys():
                for metric, value in Data["data"][scheduler].items():
                    Data["data"][scheduler][metric].append(data["data"][scheduler][metric])
        simulation += 1

    for scheduler in Data["data"].keys():
        for metric, value in Data["data"][scheduler].items():
            data = Data["data"][scheduler][metric]
            mean = round(statistics.mean(data), 2)
            std = round(statistics.stdev(data), 2)
            Data["data"][scheduler][metric] = {"mean": mean, "std": std}
    return Data


def GetDataPerLambda(NumberSimulations, NumberProcesses, lambda_):
    Data = None
    Schedulers = []
    for NumberProcess in NumberProcesses:
        data = GetMeanStd(NumberSimulations, NumberProcess, lambda_)
        if Data is None:
            Data = data
            Data.pop("NumberProcesses")
            for scheduler in Data["data"].keys():
                Schedulers.append(scheduler)
                for metric in Data["data"][scheduler].keys():
                    for type_, value in Data["data"][scheduler][metric].items():
                        # type_ is either mean or std
                        Data["data"][scheduler][metric][type_] = [value]
        else:
            for scheduler in Data["data"].keys():
                for metric in Data["data"][scheduler].keys():
                    for type_, value in Data["data"][scheduler][metric].items():
                        Data["data"][scheduler][metric][type_].append(data["data"][scheduler][metric][type_])
    return Data, Schedulers
