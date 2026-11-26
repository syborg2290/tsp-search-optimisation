
import numpy as np
import pytest

from src.random_search import random_search


@pytest.fixture
def sample_distance_matrix():
    """Create a distance matrix for three cities."""
    return np.array([
        [0, 5, 5],
        [5, 0, np.sqrt(10)],
        [5, np.sqrt(10), 0]
    ])


def test_random_search_returns_valid_route(sample_distance_matrix):
    """Check that the returned route visits every city once."""
    route, distance, history = random_search(
        sample_distance_matrix,
        iterations=100,
        seed=42
    )

    assert sorted(route.tolist()) == [0, 1, 2]
    assert distance > 0
    assert len(history) == 100


def test_random_search_is_reproducible(sample_distance_matrix):
    """Check that identical seeds produce identical results."""
    result1 = random_search(
        sample_distance_matrix,
        iterations=100,
        seed=42
    )

    result2 = random_search(
        sample_distance_matrix,
        iterations=100,
        seed=42
    )

    np.testing.assert_array_equal(result1[0], result2[0])
    assert result1[1] == result2[1]
    assert result1[2] == result2[2]


def test_best_distance_does_not_increase(sample_distance_matrix):
    """Check that the best distance never increases."""
    _, _, history = random_search(
        sample_distance_matrix,
        iterations=100,
        seed=42
    )

    assert all(
        history[i] <= history[i - 1]
        for i in range(1, len(history))
    )


def test_invalid_iterations(sample_distance_matrix):
    """Reject zero or negative iterations."""
    with pytest.raises(ValueError):
        random_search(sample_distance_matrix, iterations=0)

    with pytest.raises(ValueError):
        random_search(sample_distance_matrix, iterations=-10)


def test_non_square_matrix():
    """Reject non-square distance matrices."""
    matrix = np.array([
        [0, 5, 3],
        [5, 0, 4]
    ])

    with pytest.raises(ValueError):
        random_search(matrix)


def test_empty_matrix():
    """Reject an empty distance matrix."""
    with pytest.raises(ValueError):
        random_search(np.array([]))


def test_negative_distances():
    """Reject negative distances."""
    matrix = np.array([
        [0, -5],
        [-5, 0]
    ])

    with pytest.raises(ValueError):
        random_search(matrix)


def test_non_finite_distances():
    """Reject non-finite distances."""
    matrix = np.array([
        [0, np.inf],
        [np.inf, 0]
    ])

    with pytest.raises(ValueError):
        random_search(matrix)
