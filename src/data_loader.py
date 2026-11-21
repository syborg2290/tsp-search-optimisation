
from pathlib import Path

import pandas as pd
import numpy as np


def load_cities(csv_path: str | Path) -> pd.DataFrame:
    """
    Load city data from a CSV file.

    Args:
        csv_path: Path to the cities CSV file.

    Returns:
        A pandas DataFrame containing the city data.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the CSV file is empty or contains no columns.
    """
    csv_path = Path(csv_path)

    # Check whether the file exists
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {csv_path}"
        )

    # Load the CSV file
    cities = pd.read_csv(csv_path)

    # Check whether the dataset is empty
    if cities.empty:
        raise ValueError("The dataset is empty.")

    # Check whether the CSV contains columns
    if len(cities.columns) == 0:
        raise ValueError("The dataset contains no columns.")

    return cities


def inspect_cities(cities: pd.DataFrame) -> None:
    """
    Display basic information about the city dataset.
    """

    print("\n========== DATASET OVERVIEW ==========")

    print(f"Number of cities/records: {len(cities)}")
    print(f"Number of columns: {len(cities.columns)}")

    print("\n========== COLUMN NAMES ==========")
    print(cities.columns.tolist())

    print("\n========== FIRST FIVE RECORDS ==========")
    print(cities.head())

    print("\n========== DATA TYPES ==========")
    print(cities.dtypes)

    print("\n========== MISSING VALUES ==========")
    print(cities.isnull().sum())

    print("\n========== DUPLICATE ROWS ==========")
    print(cities.duplicated().sum())

    print("\n========== STATISTICAL SUMMARY ==========")
    print(cities.describe(include="all"))


def validate_cities(cities: pd.DataFrame) -> None:
    """
    Validate the city dataset before TSP experiments.
    """

    required_columns = {"City", "X", "Y"}

    # Check required columns
    missing_columns = required_columns - set(cities.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Check city identifiers
    if cities["City"].isna().any():
        raise ValueError("City names contain missing values.")

    if cities["City"].duplicated().any():
        raise ValueError("Duplicate city names detected.")

    # Check coordinate data types
    if not pd.api.types.is_numeric_dtype(cities["X"]):
        raise ValueError("X coordinates must be numeric.")

    if not pd.api.types.is_numeric_dtype(cities["Y"]):
        raise ValueError("Y coordinates must be numeric.")

    # Check finite coordinate values
    coordinates = cities[["X", "Y"]].to_numpy(dtype=float)

    if not np.isfinite(coordinates).all():
        raise ValueError(
            "Coordinates contain NaN or infinite values."
        )

    # Check duplicate coordinate locations
    if cities.duplicated(subset=["X", "Y"]).any():
        raise ValueError("Duplicate coordinate locations detected.")

    print("Dataset validation successful.")



if __name__ == "__main__":

    # Resolve the project root from this Python file
    project_root = Path(__file__).resolve().parent.parent

    # Dataset location
    dataset_path = project_root / "data" / "raw" / "cities.csv"

    # Load and inspect the dataset
    city_data = load_cities(dataset_path)

    validate_cities(city_data)

    inspect_cities(city_data)
