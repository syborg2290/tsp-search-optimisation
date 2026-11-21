
import numpy as np


def calculate_route_distance(
    route: list[int],
    distance_matrix: np.ndarray
) -> float:
    """
    Calculate the total distance of a closed TSP route.

    Args:
        route: Ordered list of city indices. Each city must
               appear exactly once.
        distance_matrix: Square matrix containing pairwise
                         distances between cities.

    Returns:
        Total distance of the route, including the return
        to the starting city.

    Raises:
        ValueError: If the route or distance matrix is invalid.
    """
    distance_matrix = np.asarray(distance_matrix)

    if distance_matrix.ndim != 2:
        raise ValueError("Distance matrix must be two-dimensional.")

    rows, columns = distance_matrix.shape

    if rows != columns:
        raise ValueError("Distance matrix must be square.")

    if rows == 0:
        raise ValueError("Distance matrix cannot be empty.")

    if not np.issubdtype(distance_matrix.dtype, np.number):
        raise ValueError("Distance matrix must contain numeric values.")

    if not np.isfinite(distance_matrix).all():
        raise ValueError("Distance matrix must contain finite values.")

    route = np.asarray(route)

    if route.ndim != 1:
        raise ValueError("Route must be a one-dimensional sequence.")

    if len(route) != rows:
        raise ValueError(
            "Route must contain every city exactly once."
        )

    if not np.issubdtype(route.dtype, np.integer):
        raise ValueError("Route must contain integer city indices.")

    if not np.array_equal(np.sort(route), np.arange(rows)):
        raise ValueError(
            "Route must contain each city index exactly once."
        )

    next_cities = np.roll(route, -1)

    total_distance = np.sum(
        distance_matrix[route, next_cities]
    )

    return float(total_distance)
