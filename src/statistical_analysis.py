
from itertools import combinations

import pandas as pd
from scipy.stats import kruskal, mannwhitneyu


def holm_correction(p_values):
    """Apply Holm-Bonferroni correction to a list of p-values."""
    p_values = list(p_values)
    number_of_tests = len(p_values)

    sorted_indices = sorted(
        range(number_of_tests),
        key=lambda index: p_values[index]
    )

    adjusted = [0.0] * number_of_tests
    running_max = 0.0

    for rank, index in enumerate(sorted_indices):
        adjusted_value = (
            (number_of_tests - rank) * p_values[index]
        )
        running_max = max(running_max, adjusted_value)
        adjusted[index] = min(running_max, 1.0)

    return adjusted


def analyse_algorithm_performance(results):
    """
    Perform Kruskal-Wallis and pairwise Mann-Whitney U tests
    for each dataset size.
    """
    overall_results = []
    pairwise_results = []

    algorithms = [
        "Genetic Algorithm",
        "Simulated Annealing",
        "Random Search"
    ]

    for dataset_size in sorted(results["dataset_size"].unique()):
        subset = results[
            results["dataset_size"] == dataset_size
        ]

        groups = [
            subset.loc[
                subset["algorithm"] == algorithm,
                "best_distance"
            ].dropna()
            for algorithm in algorithms
        ]

        # Overall comparison
        statistic, p_value = kruskal(*groups)

        overall_results.append({
            "dataset_size": dataset_size,
            "kruskal_statistic": statistic,
            "p_value": p_value,
            "significant": p_value < 0.05
        })

        # Pairwise comparisons
        comparisons = []

        for algorithm_a, algorithm_b in combinations(algorithms, 2):
            values_a = subset.loc[
                subset["algorithm"] == algorithm_a,
                "best_distance"
            ].dropna()

            values_b = subset.loc[
                subset["algorithm"] == algorithm_b,
                "best_distance"
            ].dropna()

            test = mannwhitneyu(
                values_a,
                values_b,
                alternative="two-sided"
            )

            # Positive effect means algorithm A tends to
            # produce larger (worse) distances than B.
            effect_size = (
                2 * test.statistic / (len(values_a) * len(values_b))
            ) - 1

            comparisons.append({
                "dataset_size": dataset_size,
                "algorithm_a": algorithm_a,
                "algorithm_b": algorithm_b,
                "u_statistic": test.statistic,
                "p_value": test.pvalue,
                "rank_biserial_effect": effect_size
            })

        adjusted_p_values = holm_correction(
            [item["p_value"] for item in comparisons]
        )

        for item, adjusted_p in zip(
            comparisons, adjusted_p_values
        ):
            item["adjusted_p_value"] = adjusted_p
            item["significant"] = adjusted_p < 0.05
            pairwise_results.append(item)

    return (
        pd.DataFrame(overall_results),
        pd.DataFrame(pairwise_results)
    )


if __name__ == "__main__":
    results_path = "results/raw/experiment_results.csv"

    results = pd.read_csv(results_path)

    overall, pairwise = analyse_algorithm_performance(results)

    # Apply Holm correction across all dataset sizes
    overall["holm_adjusted_p_value"] = holm_correction(
        overall["p_value"].tolist()
    )

    overall["holm_significant"] = (
        overall["holm_adjusted_p_value"] < 0.05
    )

    pairwise["holm_adjusted_all_sizes"] = holm_correction(
        pairwise["p_value"].tolist()
    )

    pairwise["holm_significant_all_sizes"] = (
        pairwise["holm_adjusted_all_sizes"] < 0.05
    )

    overall.to_csv(
        "results/summary/kruskal_wallis_results.csv",
        index=False
    )

    pairwise.to_csv(
        "results/summary/pairwise_statistical_results.csv",
        index=False
    )

    overall.to_csv(
        "results/summary/kruskal_wallis_results.csv",
        index=False
    )

    pairwise.to_csv(
        "results/summary/pairwise_statistical_results.csv",
        index=False
    )

    print("\n========== KRUSKAL-WALLIS RESULTS ==========")
    print(overall.to_string(index=False))

    print("\n========== PAIRWISE COMPARISONS ==========")
    print(pairwise.to_string(index=False))
