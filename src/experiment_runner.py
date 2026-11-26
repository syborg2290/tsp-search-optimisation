
import json
import time
from pathlib import Path

import pandas as pd

from src.data_loader import load_cities
from src.distance import calculate_distance_matrix
from src.random_search import random_search
from src.simulated_annealing import simulated_annealing
from src.genetic_algorithm import genetic_algorithm


DATASET_SIZES = [10, 20, 30, 40, 50]
NUMBER_OF_RUNS = 30
EVALUATION_BUDGET = 50_000
BASE_SEED = 42


def run_experiments(dataset_path: str | Path) -> pd.DataFrame:
    """
    Run Random Search, Simulated Annealing, and Genetic Algorithm
    across all dataset sizes and independent random seeds.

    Save individual experiment results, summary statistics,
    and best routes to the results directory.
    """
    cities = load_cities(dataset_path)

    required_sizes = max(DATASET_SIZES)

    if len(cities) < required_sizes:
        raise ValueError(
            f"Dataset must contain at least {required_sizes} cities."
        )

    results = []

    # Create output directories.
    project_root = Path(__file__).resolve().parent.parent

    raw_dir = project_root / "results" / "raw"
    summary_dir = project_root / "results" / "summary"
    routes_dir = project_root / "results" / "best_routes"

    for directory in [raw_dir, summary_dir, routes_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    for dataset_size in DATASET_SIZES:

        print(f"\n========== DATASET: {dataset_size} CITIES ==========")

        # Select the first N cities.
        dataset = cities.iloc[:dataset_size].reset_index(drop=True)

        # Calculate the distance matrix once per dataset size.
        distance_matrix = calculate_distance_matrix(dataset)

        algorithms = {
            "Random Search": lambda seed: random_search(
                distance_matrix=distance_matrix,
                iterations=EVALUATION_BUDGET,
                seed=seed
            ),

            "Simulated Annealing": lambda seed: simulated_annealing(
                distance_matrix=distance_matrix,
                iterations=EVALUATION_BUDGET,
                initial_temperature=1000.0,
                cooling_rate=0.9999,
                min_temperature=0.001,
                seed=seed
            ),

            "Genetic Algorithm": lambda seed: genetic_algorithm(
                distance_matrix=distance_matrix,
                population_size=100,
                generations=499,
                crossover_rate=0.9,
                mutation_rate=0.1,
                tournament_size=3,
                seed=seed
            )
        }

        for algorithm_name, algorithm_function in algorithms.items():

            print(f"\nRunning {algorithm_name}...")

            for run_number in range(NUMBER_OF_RUNS):

                seed = BASE_SEED + run_number

                start_time = time.perf_counter()

                best_route, best_distance, history = (
                    algorithm_function(seed)
                )

                execution_time = time.perf_counter() - start_time

                # Record actual evaluations.
                if algorithm_name == "Genetic Algorithm":
                    evaluations = 100 * (499 + 1)
                else:
                    evaluations = len(history)

                if evaluations != EVALUATION_BUDGET:
                    raise RuntimeError(
                        f"{algorithm_name} used {evaluations} "
                        f"evaluations instead of {EVALUATION_BUDGET}."
                    )

                # Convert city indices into city names.
                city_sequence = dataset.iloc[best_route]["City"].tolist()

                # Close the route.
                closed_sequence = city_sequence + [city_sequence[0]]

                results.append({
                    "dataset_size": dataset_size,
                    "algorithm": algorithm_name,
                    "run": run_number + 1,
                    "seed": seed,
                    "best_distance": best_distance,
                    "execution_time": execution_time,
                    "evaluations": evaluations,
                    "best_route_indices": json.dumps(
                        best_route.tolist()
                    ),
                    "best_city_sequence": json.dumps(
                        closed_sequence
                    )
                })

                print(
                    f"Run {run_number + 1:02d}/{NUMBER_OF_RUNS} | "
                    f"Distance: {best_distance:.4f} | "
                    f"Time: {execution_time:.4f}s"
                )

    # Convert results to a DataFrame.
    results_df = pd.DataFrame(results)

    # Save individual experiment results.
    results_df.to_csv(
        raw_dir / "experiment_results.csv",
        index=False
    )

    # Calculate summary statistics.
    summary_df = (
        results_df
        .groupby(["dataset_size", "algorithm"])
        .agg(
            best_distance=("best_distance", "min"),
            mean_distance=("best_distance", "mean"),
            std_distance=("best_distance", "std"),
            mean_execution_time=("execution_time", "mean"),
            std_execution_time=("execution_time", "std"),
            number_of_runs=("run", "count"),
            evaluations=("evaluations", "first")
        )
        .reset_index()
    )

    summary_df.to_csv(
        summary_dir / "experiment_summary.csv",
        index=False
    )

    # Save the best route from each algorithm and dataset size.
    best_routes_df = (
        results_df
        .loc[
            results_df.groupby(
                ["dataset_size", "algorithm"]
            )["best_distance"].idxmin()
        ]
        .reset_index(drop=True)
    )

    best_routes_df.to_csv(
        routes_dir / "best_routes.csv",
        index=False
    )

    print("\n========== EXPERIMENTS COMPLETED ==========")
    print(summary_df.to_string(index=False))

    return results_df


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent

    dataset_path = project_root / "data" / "raw" / "cities.csv"

    run_experiments(dataset_path)
