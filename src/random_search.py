
import numpy as np

from src.route_evaluator import calculate_route_distance


def random_search(
    distance_matrix: np.ndarray,
    iterations: int = 1000,
    seed: int | None = None
) -> tuple[np.ndarray, float, list[float]]:
    """
    Find a short TSP route using random search.

    Args:
        distance_matrix: Pairwise distances between cities.
        iterations: Number of candidate routes to evaluate.
        seed: Random seed for reproducibility.

    Returns:
        A tuple containing:
        - Best route found.
        - Best route distance.
        - Best distance after each iteration.
    """
    distance_matrix = np.asarray(distance_matrix)

    if distance_matrix.ndim != 2:
        raise ValueError("Distance matrix must be two-dimensional.")

    rows, columns = distance_matrix.shape

    if rows != columns or rows == 0:
        raise ValueError("Distance matrix must be non-empty and square.")

    if not np.issubdtype(distance_matrix.dtype, np.number):
        raise ValueError("Distance matrix must contain numeric values.")

    if not np.isfinite(distance_matrix).all():
        raise ValueError("Distance matrix must contain finite values.")

    if np.any(distance_matrix < 0):
        raise ValueError("Distances cannot be negative.")

    if isinstance(iterations, bool) or not isinstance(iterations, (int, np.integer)):
        raise ValueError("Iterations must be a positive integer.")

    if iterations <= 0:
        raise ValueError("Iterations must be a positive integer.")

    rng = np.random.default_rng(seed)

    number_of_cities = rows

    best_route = None
    best_distance = float("inf")
    history = []

    for _ in range(iterations):

        # Generate a random permutation of city indices.
        candidate_route = rng.permutation(number_of_cities)

        # Calculate the complete route distance.
        candidate_distance = calculate_route_distance(
            candidate_route,
            distance_matrix
        )

        # Keep the best route found so far.
        if candidate_distance < best_distance:
            best_distance = candidate_distance
            best_route = candidate_route.copy()

        # Record the best distance after this iteration.
        history.append(best_distance)

    return best_route, best_distance, history
