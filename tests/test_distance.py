
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
import sys

# Find the project root
project_root = Path.cwd().resolve()

if project_root.name == "notebooks":
    project_root = project_root.parent

# Add project root to Python module search path
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

print("Project root:", project_root)
print("Source directory exists:", (project_root / "src").exists())

from src.distance import calculate_distance_matrix



def test_distance_matrix_values():
    """Check calculated distances against known values."""

    cities = pd.DataFrame({
        "City": ["A", "B", "C"],
        "X": [0, 3, 0],
        "Y": [0, 4, 5]
    })

    result = calculate_distance_matrix(cities)

    expected = np.array([
        [0, 5, 5],
        [5, 0, np.sqrt(10)],
        [5, np.sqrt(10), 0]
    ])

    np.testing.assert_allclose(result, expected)


def test_distance_matrix_shape():
    """Check that the matrix has the correct dimensions."""

    cities = pd.DataFrame({
        "City": ["A", "B", "C", "D"],
        "X": [0, 3, 0, 6],
        "Y": [0, 4, 5, 8]
    })

    result = calculate_distance_matrix(cities)

    assert result.shape == (4, 4)


def test_distance_matrix_diagonal():
    """Check that distances from cities to themselves are zero."""

    cities = pd.DataFrame({
        "X": [0, 3, 0],
        "Y": [0, 4, 5]
    })

    result = calculate_distance_matrix(cities)

    np.testing.assert_allclose(
        np.diag(result),
        np.zeros(3)
    )


def test_distance_matrix_symmetry():
    """Check that distance A to B equals distance B to A."""

    cities = pd.DataFrame({
        "X": [0, 3, 0],
        "Y": [0, 4, 5]
    })

    result = calculate_distance_matrix(cities)

    np.testing.assert_allclose(result, result.T)


def test_distances_are_non_negative():
    """Check that all distances are non-negative."""

    cities = pd.DataFrame({
        "X": [0, 3, 0],
        "Y": [0, 4, 5]
    })

    result = calculate_distance_matrix(cities)

    assert np.all(result >= 0)


def test_empty_dataset():
    """Check that an empty dataset raises an error."""

    cities = pd.DataFrame(columns=["X", "Y"])

    with pytest.raises(ValueError):
        calculate_distance_matrix(cities)


def test_missing_coordinate_column():
    """Check that missing coordinate columns raise an error."""

    cities = pd.DataFrame({
        "City": ["A", "B"],
        "X": [0, 3]
    })

    with pytest.raises(ValueError):
        calculate_distance_matrix(cities)


def test_non_numeric_coordinates():
    """Check that non-numeric coordinates raise an error."""

    cities = pd.DataFrame({
        "X": ["invalid", "3"],
        "Y": [0, 4]
    })

    with pytest.raises(ValueError):
        calculate_distance_matrix(cities)


def test_non_finite_coordinates():
    """Check that infinite coordinates raise an error."""

    cities = pd.DataFrame({
        "X": [0, np.inf],
        "Y": [0, 4]
    })

    with pytest.raises(ValueError):
        calculate_distance_matrix(cities)
