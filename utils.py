import os
import json


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
