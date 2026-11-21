
import numpy as np
import pandas as pd


def calculate_distance_matrix(
    cities: pd.DataFrame,
) -> np.ndarray:
    """
    Calculate the pairwise Euclidean distance matrix.

    Args:
        cities: DataFrame containing X and Y coordinates.

    Returns:
        A NumPy array containing pairwise distances.
        Matrix shape: (number_of_cities, number_of_cities).

    Raises:
        ValueError: If coordinates are missing, invalid,
                    non-numeric, or the dataset is empty.
    """

    # Check required coordinate columns
    required_columns = {"X", "Y"}

    if not required_columns.issubset(cities.columns):
        raise ValueError("Dataset must contain X and Y columns.")

    if cities.empty:
        raise ValueError("Cannot calculate distances for an empty dataset.")

    # Extract coordinates as a NumPy array
    try:
        coordinates = cities[["X", "Y"]].to_numpy(dtype=float)
    except (TypeError, ValueError) as error:
        raise ValueError("Coordinates must be numeric.") from error

    # Reject NaN and infinite values
    if not np.isfinite(coordinates).all():
        raise ValueError("Coordinates must contain finite values.")

    # Calculate pairwise coordinate differences using broadcasting
    differences = (
        coordinates[:, np.newaxis, :]
        - coordinates[np.newaxis, :, :]
    )

    # Calculate Euclidean distances
    squared_differences = np.sum(differences ** 2, axis=2)

    distance_matrix = np.sqrt(squared_differences)

    # print("Distance Matrix :: " , distance_matrix)

    return distance_matrix

