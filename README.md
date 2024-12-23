# CPUScheduling

## Project Overview

This project has been fully developed by the owner, **Dhia Neifar**, for the course **ECE 578 - Advanced Operating Systems**. The project is supervised and maintained by **Dhia Neifar**.

### Purpose
This project provides source code for various CPU scheduling algorithms, designed to simulate and evaluate their performance under different conditions. The project focuses on:
- **First Come First Serve (FCFS)**
- **Shortest Job Execution (SJE)**
- **Longest Job Execution (LJE)**
- **Non-Preemptive Priority**
- **Preemptive Priority**
- **Round Robin (RR)**
- **Shortest Remaining Time First (SRFT)**
- **Longest Remaining Burst Time (LRBT)**
- **Highest Response Ratio Next (HRRN)**

## Key Features
1. **Process Arrival Time**: Follows a Poisson distribution with varying λ values: `[1, 5, 10, 20]`.
2. **Burst Time**: Follows a Normal distribution \( N(\mu = 10, \sigma = 10) \).
3. **Process Priority**: Uniform distribution \( U([1, 10]) \), where `1` is the highest priority.
4. **Number of Processes**: Varies across `[5, 10, 20, 50, 100, ... 1000]`.
5. **Simulation Data**: Generates 500 samples for different configurations, saving results as JSON files in a folder named `Trials` with the format:
   ```
   {NumberProcesses}_{lambda_}_{SimulationID}.json
   ```
6. **Data Visualization**: Automatically generates figures from the simulation data and saves them in a folder named `Figures`.

---

## Getting Started

### Prerequisites
To get started with this project, ensure you have Python installed and set up a virtual environment.

#### Creating a Virtual Environment
- **Using `venv` (Python's built-in virtual environment tool):**
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Linux/Mac
  venv\Scripts\activate    # On Windows
  ```

- **Using Conda:**
  ```bash
  conda create -n cpuscheduling python=3.9 -y
  conda activate cpuscheduling
  ```

### Installing Dependencies
- **Install required Python packages:**
  - On Linux:
    ```bash
    pip3 install -r requirements.txt
    ```
  - On Windows/Mac:
    ```bash
    pip install -r requirements.txt
    ```

---

## Running the Simulation
1. To start the simulation, run the following command:
   ```bash
   python simulation.py
   ```
   - For Ubuntu or systems using `python3`:
     ```bash
     python3 simulation.py
     ```

2. Simulation output files will be stored in the `Trials` folder.

3. Generated figures will be saved in the `Figures` folder.

---

## Folder Structure
```plaintext
.
├── Trials/       # Stores JSON files with simulation results
├── Figures/      # Stores generated visualization figures
├── simulation.py # Main simulation script
├── requirements.txt # Python dependencies
├── README.md     # Project documentation
└── ...           # Additional project files
```

---

## Notes
- Ensure you have sufficient storage for simulation output and generated figures.
- You can modify the parameters (e.g., number of processes, λ values, priority ranges) directly in the code for custom configurations.

---

## Author
**Dhia Neifar**
