from pathlib import Path
import numpy as np
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

from src.route_evaluator import calculate_route_distance


@pytest.fixture
def sample_distance_matrix():
    """Create a known distance matrix for three cities."""
    return np.array([
        [0, 5, 5],
        [5, 0, np.sqrt(10)],
        [5, np.sqrt(10), 0]
    ])


def test_route_distance(sample_distance_matrix):
    """Check the total distance of a known route."""
    route = [0, 1, 2]

    result = calculate_route_distance(
        route,
        sample_distance_matrix
    )

    expected = 5 + np.sqrt(10) + 5

    assert result == pytest.approx(expected)


def test_route_returns_to_start(sample_distance_matrix):
    """Check that the final city connects to the first city."""
    route = [0, 1, 2]

    result = calculate_route_distance(
        route,
        sample_distance_matrix
    )

    expected = (
        sample_distance_matrix[0, 1]
        + sample_distance_matrix[1, 2]
        + sample_distance_matrix[2, 0]
    )

    assert result == pytest.approx(expected)


def test_different_route(sample_distance_matrix):
    """Check another valid city ordering."""
    route = [0, 2, 1]

    result = calculate_route_distance(
        route,
        sample_distance_matrix
    )

    assert result == pytest.approx(10 + np.sqrt(10))


def test_invalid_route_length(sample_distance_matrix):
    """Reject routes that omit cities."""
    with pytest.raises(ValueError):
        calculate_route_distance([0, 1], sample_distance_matrix)


def test_duplicate_city_in_route(sample_distance_matrix):
    """Reject routes containing duplicate city indices."""
    with pytest.raises(ValueError):
        calculate_route_distance([0, 1, 1], sample_distance_matrix)


def test_invalid_city_index(sample_distance_matrix):
    """Reject city indices outside the matrix range."""
    with pytest.raises(ValueError):
        calculate_route_distance([0, 1, 3], sample_distance_matrix)


def test_empty_distance_matrix():
    """Reject an empty distance matrix."""
    with pytest.raises(ValueError):
        calculate_route_distance([], np.array([]))


def test_non_square_distance_matrix():
    """Reject a non-square distance matrix."""
    matrix = np.array([
        [0, 5, 3],
        [5, 0, 4]
    ])

    with pytest.raises(ValueError):
        calculate_route_distance([0, 1], matrix)


def test_non_finite_distance_matrix():
    """Reject matrices containing invalid numerical values."""
    matrix = np.array([
        [0, np.inf],
        [np.inf, 0]
    ])

    with pytest.raises(ValueError):
        calculate_route_distance([0, 1], matrix)
