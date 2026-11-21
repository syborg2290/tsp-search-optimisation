# TSP Search Optimisation

A comparative study of single-solution and evolutionary search algorithms for solving the **Traveling Salesman Problem (TSP)** using Python.

## 1. Project Overview

This project investigates and compares two optimisation algorithms to solve the Traveling Salesman Problem (TSP).

The objective is to find the shortest possible route that visits every city exactly once and returns to the starting city.

The project uses a dataset containing 50 cities and evaluates algorithm performance across different problem sizes.

### Algorithms

**1. Simulated Annealing (SA)**
- Single-solution search algorithm.
- Uses neighbourhood operators to generate alternative routes.
- Uses a temperature-based acceptance mechanism.
- Can accept worse solutions to escape local optima.
- Uses a cooling schedule to gradually reduce exploration.

**2. Genetic Algorithm (GA)**
- Population-based evolutionary algorithm.
- Uses selection to choose parent solutions.
- Uses crossover to generate offspring.
- Uses mutation to maintain population diversity.
- Uses elitism to preserve the best solutions.

## 2. Project Objectives

- Implement Simulated Annealing for TSP.
- Implement a Genetic Algorithm for TSP.
- Experiment with different optimisation parameters.
- Compare solution quality and execution time.
- Evaluate algorithm robustness and scalability.
- Perform statistical analysis on experimental results.
- Visualise algorithm performance and convergence.

## 3. Technologies

| Technology | Purpose |
|---|---|
| Python 3 | Programming language |
| NumPy | Numerical computations |
| Pandas | Dataset processing |
| Matplotlib | Data visualisation |
| Seaborn | Statistical visualisation |
| SciPy | Statistical analysis |
| JupyterLab | Interactive experimentation |
| Pytest | Unit testing |
| Ruff | Code quality and linting |
| Git & GitHub | Version control |

## 4. Development Environment Setup

### Prerequisites

- Python 3
- Git
- Visual Studio Code (recommended)

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/tsp-search-optimisation.git
cd tsp-search-optimisation
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

For Windows CMD:

```cmd
venv\Scripts\activate.bat
```

### Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Install dependencies

```bash
python -m pip install numpy pandas matplotlib seaborn scipy jupyterlab pytest ruff
```

### Save dependencies

```bash
python -m pip freeze > requirements.txt
```

### Install dependencies from requirements.txt

```bash
python -m pip install -r requirements.txt
```

## 5. Experimental Roadmap

The project is divided into six experimental phases.

| Phase | Description | Status |
|---|---|---|
| 1 | Dataset exploration and inspection | Planned |
| 2 | TSP formulation and distance calculation | Planned |
| 3 | Random search baseline | Planned |
| 4 | Simulated Annealing implementation and experiments | Planned |
| 5 | Genetic Algorithm implementation and experiments | Planned |
| 6 | Algorithm comparison and statistical analysis | Planned |

### Dataset Sizes

Both algorithms will be evaluated using five different problem sizes:

- 10 cities
- 20 cities
- 30 cities
- 40 cities
- 50 cities

### Experimental Evaluation

The following metrics will be investigated:

- Best route distance
- Mean route distance
- Standard deviation
- Execution time
- Convergence behaviour
- Robustness
- Scalability

At least 30 independent runs will be conducted for each stochastic algorithm, following a consistent experimental protocol.

## 6. Repository Structure

```text
tsp-search-optimisation/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│
├── src/
│   ├── algorithms/
│   ├── evaluation/
│   └── utils/
│
├── tests/
│
├── notebooks/
│
├── experiments/
│
├── results/
│   ├── raw/
│   ├── processed/
│   ├── figures/
│   └── routes/
│
└── report/
```

## 7. Current Development Progress

- [x] Project name and objectives defined
- [x] Algorithm selection: Simulated Annealing and Genetic Algorithm
- [x] Python virtual environment created
- [x] Virtual environment activated
- [ ] Project dependencies installed
- [ ] Dataset exploration
- [ ] TSP problem formulation
- [ ] Algorithm implementation
- [ ] Experimental evaluation
- [ ] Statistical comparison
- [ ] Final report and presentation

## 8. Expected Outcomes

The project aims to establish an experimental comparison of Simulated Annealing and Genetic Algorithm for solving TSP instances of different sizes.

The final evaluation will identify their relative strengths, limitations and suitability under different computational constraints.

## 9. Academic Context

**Module:** UFCEL1-15-M – AI for Search and Optimisation

**Assessment:** Practical Skill Assessment 2026

**Problem:** Traveling Salesman Problem (TSP)


## 10. Testing With Pytest

**Example** python -m pytest tests/test_distance.py -v

Running the Tests

Run all unit tests:

python -m pytest -v

Run the distance calculator tests specifically:

python -m pytest tests/test_distance.py -v

---

*This repository documents the development, implementation and experimental evaluation of the optimisation algorithms as part of an academic project.*