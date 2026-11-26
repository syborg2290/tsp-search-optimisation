# TSP Search and Optimisation

## AI for Search and Optimisation – Practical Skill Assessment 2026

This project investigates the Travelling Salesperson Problem (TSP) using search and optimisation algorithms. It compares Simulated Annealing (SA) and a Genetic Algorithm (GA), using Random Search as a baseline.

The experiments evaluate solution quality, execution time, convergence, statistical significance, and scalability across different problem sizes.

---

## 1. Project Objectives

- Implement a TSP solution using Simulated Annealing.
- Implement a TSP solution using a Genetic Algorithm.
- Implement Random Search as a baseline.
- Calculate pairwise Euclidean distances between cities.
- Evaluate closed TSP routes.
- Compare algorithms using consistent evaluation budgets.
- Run at least 30 independent experiments per algorithm and dataset size.
- Perform statistical tests to evaluate performance differences.
- Visualise solution quality, execution time, and convergence.

## 2. Algorithms

| Algorithm | Category | Purpose |
|---|---|---|
| Random Search | Baseline | Evaluates randomly generated routes |
| Simulated Annealing | Single-solution search | Explores neighbouring routes using a temperature-based acceptance strategy |
| Genetic Algorithm | Evolutionary algorithm | Evolves a population using selection, crossover, mutation, and elitism |

## 3. Dataset

The project uses `cities.csv`, containing 50 cities.

| Column | Description |
|---|---|
| City | City identifier |
| X | X coordinate |
| Y | Y coordinate |

Dataset sizes used in the experiments:

- 10 cities
- 20 cities
- 30 cities
- 40 cities
- 50 cities

The objective is to minimise the total Euclidean distance of a closed route, including the return from the last city to the starting city.

## 4. Project Structure

```text
tsp-search-optimisation/
│
├── data/
│   └── raw/
│       └── cities.csv
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   └── 02_experimental_analysis.ipynb
│
├── results/
│   ├── raw/
│   ├── summary/
│   └── best_routes/
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── distance.py
│   ├── route_evaluator.py
│   ├── random_search.py
│   ├── simulated_annealing.py
│   ├── genetic_algorithm.py
│   ├── experiment_runner.py
│   └── statistical_analysis.py
│
├── tests/
│
├── .gitignore
├── README.md
└── requirements.txt
```

## 5. Development Environment

- Python 3.14
- Visual Studio Code
- Jupyter Notebook
- NumPy
- Pandas
- Matplotlib
- Seaborn
- SciPy
- Pytest

The project uses a Python virtual environment named `venv`.

---

# 6. Commands Reference

All commands below are intended for **Windows PowerShell**, unless otherwise stated.

Run commands from the root directory of the repository:

```powershell
cd C:\Users\kasun\Desktop\projects\tsp-search-optimisation
```

Replace the example path with your actual project location.

## 6.1 Clone the GitHub Repository

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Move into the project directory:

```powershell
cd tsp-search-optimisation
```

Open the project in VS Code:

```powershell
code .
```

## 6.2 Check Python and Git

Check the Python version:

```powershell
python --version
```

Check which Python executable is being used:

```powershell
where.exe python
```

Check Git:

```powershell
git --version
```

## 6.3 Create a Virtual Environment

Create the environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, temporarily allow activation scripts for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Activate again:

```powershell
.\venv\Scripts\Activate.ps1
```

For Windows Command Prompt instead of PowerShell:

```cmd
venv\Scripts\activate.bat
```

Check the active Python interpreter:

```powershell
where.exe python
```

The path should point to the project's `venv` directory.

## 6.4 Install and Manage Dependencies

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install the project dependencies:

```powershell
pip install numpy pandas matplotlib seaborn scipy jupyterlab pytest ruff
```

Alternatively, install dependencies from the requirements file:

```powershell
pip install -r requirements.txt
```

Update `requirements.txt` after installing or changing dependencies:

```powershell
python -m pip freeze > requirements.txt
```

Check installed packages:

```powershell
pip list
```

Check a particular package:

```powershell
pip show numpy
```

## 6.5 Start Jupyter Notebook

Start JupyterLab:

```powershell
jupyter lab
```

Alternatively, start the classic Jupyter Notebook interface:

```powershell
jupyter notebook
```

Open a particular notebook:

```powershell
jupyter notebook notebooks/01_data_exploration.ipynb
```

```powershell
jupyter notebook notebooks/02_experimental_analysis.ipynb
```

To register the virtual environment as a notebook kernel, install the kernel package:

```powershell
pip install ipykernel
```

Register the environment:

```powershell
python -m ipykernel install --user --name tsp-search-optimisation --display-name "Python (TSP Optimisation)"
```

In VS Code, select the `Python (TSP Optimisation)` kernel when running the notebooks.

## 6.6 Run Dataset Exploration

Run the data loader:

```powershell
python -m src.data_loader
```

This checks and displays the dataset information, including:

- Number of records.
- Column names.
- Data types.
- Missing values.
- Duplicate records.
- Descriptive statistics.

Open the exploration notebook:

```powershell
jupyter notebook notebooks/01_data_exploration.ipynb
```

## 6.7 Run Automated Tests

Run the complete test suite:

```powershell
python -m pytest -v
```

Run tests with a short summary:

```powershell
python -m pytest -q
```

Run a particular test file:

```powershell
python -m pytest tests/test_distance.py -v
```

```powershell
python -m pytest tests/test_route_evaluator.py -v
```

```powershell
python -m pytest tests/test_random_search.py -v
```

```powershell
python -m pytest tests/test_simulated_annealing.py -v
```

```powershell
python -m pytest tests/test_genetic_algorithm.py -v
```

Run tests and display a coverage report if `pytest-cov` is installed:

```powershell
pip install pytest-cov
```

```powershell
python -m pytest --cov=src --cov-report=term-missing
```

## 6.8 Run the Experiment Runner

The experiment runner executes the optimisation algorithms across the five dataset sizes.

Run:

```powershell
python -m src.experiment_runner
```

Current experimental configuration:

| Setting | Value |
|---|---:|
| Dataset sizes | 10, 20, 30, 40, 50 |
| Independent runs | 30 |
| Evaluation budget | 50,000 |
| Random Search iterations | 50,000 |
| SA iterations | 50,000 |
| GA population size | 100 |
| GA generations | 499 |
| GA crossover rate | 0.9 |
| GA mutation rate | 0.1 |
| GA tournament size | 3 |
| Base seed | 42 |

The experiment design produces 450 individual algorithm runs:

```text
3 algorithms × 5 dataset sizes × 30 runs = 450 experiments
```

Allow the experiment runner to finish before analysing the generated results.

## 6.9 Run Statistical Analysis

Run the statistical analysis module:

```powershell
python -m src.statistical_analysis
```

The statistical analysis compares the final route-distance distributions.

Tests used:

- Kruskal-Wallis test for an overall comparison between the three algorithms.
- Mann-Whitney U tests for pairwise comparisons.
- Holm correction for multiple comparisons.
- Rank-biserial effect size to assess the magnitude and direction of pairwise differences.

The statistical analysis should report the test statistics, p-values, adjusted p-values, effect sizes, and significance decisions.

## 6.10 Open the Experimental Analysis Notebook

```powershell
jupyter notebook notebooks/02_experimental_analysis.ipynb
```

This notebook is used to inspect the experimental data, statistical results, and visualisations.

---

# 7. Generated Results

After the experiment runner and statistical analysis have completed, inspect the `results/` directory.

Expected result files include:

| File | Description |
|---|---|
| `results/raw/experiment_results.csv` | Individual experiment records |
| `results/summary/experiment_summary.csv` | Best, mean, standard deviation, and execution-time summaries |
| `results/best_routes/best_routes.csv` | Best-found routes for each algorithm and dataset size |
| `results/summary/kruskal_wallis_results.csv` | Overall statistical comparison |
| `results/summary/pairwise_statistical_results.csv` | Pairwise statistical comparisons |

Expected record counts:

| File | Expected records |
|---|---:|
| Individual experiment results | 450 |
| Experiment summary | 15 |
| Best routes | 15 |
| Kruskal-Wallis results | 5 |
| Pairwise comparisons | 15 |

The statistical output filenames should match the filenames configured in `statistical_analysis.py`.

## 7.1 Load Experimental Results Using Python

```python
import pandas as pd

results = pd.read_csv(
    "results/raw/experiment_results.csv"
)

summary = pd.read_csv(
    "results/summary/experiment_summary.csv"
)

best_routes = pd.read_csv(
    "results/best_routes/best_routes.csv"
)

print("Individual experiments:", len(results))
print("Summary records:", len(summary))
print("Best routes:", len(best_routes))

display(summary)
```

## 7.2 Inspect the Best Routes

```python
display(best_routes)
```

## 7.3 Inspect the Statistical Results

```python
kruskal_results = pd.read_csv(
    "results/summary/kruskal_wallis_results.csv"
)

pairwise_results = pd.read_csv(
    "results/summary/pairwise_statistical_results.csv"
)

display(kruskal_results)
display(pairwise_results)
```

## 7.4 Check the Experimental Data

```python
print(results.info())

print(results.isnull().sum())

print(results.groupby(
    ["dataset_size", "algorithm"]
).size())
```

---

# 8. Git Commands and Version Control

Use Git to track project development and maintain meaningful commits.

Check the current working tree:

```powershell
git status
```

View changed files:

```powershell
git diff
```

View the latest commit:

```powershell
git log -1 --oneline
```

View the commit history:

```powershell
git log --oneline
```

Stage a particular file:

```powershell
git add README.md
```

Stage multiple files:

```powershell
git add src/ tests/ notebooks/
```

Stage all changes:

```powershell
git add .
```

Commit changes:

```powershell
git commit -m "Describe the changes made"
```

Push changes to GitHub:

```powershell
git push
```

Pull the latest changes:

```powershell
git pull
```

Check the current branch:

```powershell
git branch
```

Create a new branch:

```powershell
git switch -c feature/branch-name
```

Switch branches:

```powershell
git switch main
```

If your default branch is named `development`, use that name instead of `main`.

## 8.1 Suggested Commit Messages

Use clear messages describing each milestone:

```powershell
git commit -m "Set up project structure and Python environment"
```

```powershell
git commit -m "Add dataset loading and validation"
```

```powershell
git commit -m "Add Euclidean distance matrix calculation"
```

```powershell
git commit -m "Implement TSP route evaluator"
```

```powershell
git commit -m "Implement random search baseline"
```

```powershell
git commit -m "Implement simulated annealing"
```

```powershell
git commit -m "Implement genetic algorithm"
```

```powershell
git commit -m "Add experimental evaluation runner"
```

```powershell
git commit -m "Add statistical analysis and visualisations"
```

```powershell
git commit -m "Update README with project commands and documentation"
```

---

# 9. Code Quality

Run Ruff to check Python code:

```powershell
ruff check .
```

Automatically fix supported issues:

```powershell
ruff check . --fix
```

Check formatting:

```powershell
ruff format --check .
```

Format Python files:

```powershell
ruff format .
```

Run tests after making code changes:

```powershell
python -m pytest -v
```

---

# 10. Deactivate the Virtual Environment

When finished working:

```powershell
deactivate
```

To reactivate the environment when returning to the project:

```powershell
.\venv\Scripts\Activate.ps1
```

---

# 11. Recommended Workflow

Follow this order when working on the project.

| Step | Task | Command |
|---|---|---|
| 1 | Activate virtual environment | `.\venv\Scripts\Activate.ps1` |
| 2 | Install dependencies | `pip install -r requirements.txt` |
| 3 | Inspect dataset | `python -m src.data_loader` |
| 4 | Open exploration notebook | `jupyter notebook notebooks/01_data_exploration.ipynb` |
| 5 | Run all tests | `python -m pytest -v` |
| 6 | Execute experiments | `python -m src.experiment_runner` |
| 7 | Run statistical analysis | `python -m src.statistical_analysis` |
| 8 | Open analysis notebook | `jupyter notebook notebooks/02_experimental_analysis.ipynb` |
| 9 | Check code quality | `ruff check .` |
| 10 | Check Git changes | `git status` |
| 11 | Commit changes | `git add .` followed by `git commit -m "..."` |
| 12 | Push to GitHub | `git push` |

---

# 12. Important Notes

- Always activate the project's virtual environment before running Python commands.
- Run commands from the repository root directory.
- Keep the original dataset in `data/raw/cities.csv`.
- Do not manually modify experimental results to improve reported performance.
- Preserve raw experiment records and random seeds.
- Use the same evaluation budget when comparing algorithms.
- Report the best-found solution accurately; do not claim global optimality without an exact proof.
- Run the complete test suite after modifying algorithm implementations.
- Keep generated result files and notebooks organised.
- Use meaningful Git commits to document development progress.

## 13. Project Status

The project includes dataset exploration, distance calculation, route evaluation, Random Search, Simulated Annealing, Genetic Algorithm, experimental evaluation, statistical analysis, and result visualisation.

The final assessment report should explain the algorithms, experimental methodology, parameter tuning, results, statistical findings, scalability, limitations, and conclusions.

---

**Module:** UFCEL1-15-M – AI for Search and Optimisation  
**Assessment:** Practical Skill Assessment 2026  
**Project:** Travelling Salesperson Problem – Search and Optimisation
