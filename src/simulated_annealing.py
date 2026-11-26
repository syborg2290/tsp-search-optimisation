
import math

import numpy as np

from src.route_evaluator import calculate_route_distance


def simulated_annealing(
    distance_matrix: np.ndarray,
    iterations: int = 10000,
    initial_temperature: float = 1000.0,
    cooling_rate: float = 0.995,
    min_temperature: float = 0.001,
    seed: int | None = None
) -> tuple[np.ndarray, float, list[float]]:
    """
    Find a short TSP route using Simulated Annealing.

    Args:
        distance_matrix: Pairwise distances between cities.
        iterations: Maximum number of candidate routes to evaluate.
        initial_temperature: Starting acceptance temperature.
        cooling_rate: Temperature multiplier after each iteration.
        min_temperature: Minimum temperature before stopping.
        seed: Random seed for reproducibility.

    Returns:
        Best route, best distance, and best-distance history.
    """
    distance_matrix = np.asarray(distance_matrix)

    if distance_matrix.ndim != 2:
        raise ValueError("Distance matrix must be two-dimensional.")

    rows, columns = distance_matrix.shape

    if rows == 0 or rows != columns:
        raise ValueError("Distance matrix must be non-empty and square.")

    if not np.issubdtype(distance_matrix.dtype, np.number):
        raise ValueError("Distance matrix must contain numeric values.")

    if not np.isfinite(distance_matrix).all():
        raise ValueError("Distance matrix must contain finite values.")

    if np.any(distance_matrix < 0):
        raise ValueError("Distances cannot be negative.")

    if isinstance(iterations, bool) or not isinstance(
        iterations, (int, np.integer)
    ) or iterations <= 0:
        raise ValueError("Iterations must be a positive integer.")

    if not math.isfinite(initial_temperature) or initial_temperature <= 0:
        raise ValueError("Initial temperature must be positive and finite.")

    if not math.isfinite(min_temperature) or min_temperature <= 0:
        raise ValueError("Minimum temperature must be positive and finite.")

    if min_temperature >= initial_temperature:
        raise ValueError(
            "Minimum temperature must be lower than initial temperature."
        )

    if not math.isfinite(cooling_rate) or not 0 < cooling_rate < 1:
        raise ValueError("Cooling rate must be between 0 and 1.")

    rng = np.random.default_rng(seed)

    number_of_cities = rows

    # Generate the initial random route.
    current_route = rng.permutation(number_of_cities)
    current_distance = calculate_route_distance(
        current_route,
        distance_matrix
    )

    # Initially, the current route is also the best route.
    best_route = current_route.copy()
    best_distance = current_distance

    temperature = initial_temperature
    history = []

    for _ in range(iterations):

        # Stop when the temperature reaches its minimum.
        if temperature <= min_temperature:
            break

        # Generate a neighbouring route by swapping two cities.
        candidate_route = current_route.copy()

        city_a, city_b = rng.choice(
            number_of_cities,
            size=2,
            replace=False
        )

        candidate_route[city_a], candidate_route[city_b] = (
            candidate_route[city_b],
            candidate_route[city_a]
        )

        # Evaluate the candidate route.
        candidate_distance = calculate_route_distance(
            candidate_route,
            distance_matrix
        )

        delta = candidate_distance - current_distance

        # Always accept improvements.
        if delta < 0:
            accept_candidate = True

        # Sometimes accept worse solutions.
        else:
            acceptance_probability = math.exp(
                -delta / temperature
            )

            accept_candidate = (
                rng.random() < acceptance_probability
            )

        if accept_candidate:
            current_route = candidate_route
            current_distance = candidate_distance

        # Update the best solution found so far.
        if current_distance < best_distance:
            best_route = current_route.copy()
            best_distance = current_distance

        # Record the best distance after this iteration.
        history.append(best_distance)

        # Reduce the temperature.
        temperature *= cooling_rate

    return best_route, best_distance, history
