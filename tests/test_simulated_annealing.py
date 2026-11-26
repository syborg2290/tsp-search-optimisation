
import numpy as np
import pytest

from src.simulated_annealing import simulated_annealing


@pytest.fixture
def sample_distance_matrix():
    """Create a distance matrix for three cities."""
    return np.array([
        [0, 5, 5],
        [5, 0, np.sqrt(10)],
        [5, np.sqrt(10), 0]
    ])


def test_returns_valid_route(sample_distance_matrix):
    """Check that every city appears exactly once."""
    route, distance, history = simulated_annealing(
        sample_distance_matrix,
        iterations=1000,
        seed=42
    )

    assert sorted(route.tolist()) == [0, 1, 2]
    assert distance > 0
    assert len(history) > 0


def test_reproducible_results(sample_distance_matrix):
    """Check that the same seed produces the same result."""
    result1 = simulated_annealing(
        sample_distance_matrix,
        iterations=1000,
        seed=42
    )

    result2 = simulated_annealing(
        sample_distance_matrix,
        iterations=1000,
        seed=42
    )

    np.testing.assert_array_equal(result1[0], result2[0])
    assert result1[1] == result2[1]
    assert result1[2] == result2[2]


def test_best_distance_never_increases(sample_distance_matrix):
    """Check that best-distance history is non-increasing."""
    _, _, history = simulated_annealing(
        sample_distance_matrix,
        iterations=1000,
        seed=42
    )

    assert all(
        history[i] <= history[i - 1]
        for i in range(1, len(history))
    )


def test_invalid_iterations(sample_distance_matrix):
    """Reject zero or negative iteration counts."""
    with pytest.raises(ValueError):
        simulated_annealing(
            sample_distance_matrix,
            iterations=0
        )

    with pytest.raises(ValueError):
        simulated_annealing(
            sample_distance_matrix,
            iterations=-10
        )


def test_invalid_cooling_rate(sample_distance_matrix):
    """Reject cooling rates outside the valid range."""
    with pytest.raises(ValueError):
        simulated_annealing(
            sample_distance_matrix,
            cooling_rate=1.0
        )


def test_invalid_initial_temperature(sample_distance_matrix):
    """Reject non-positive initial temperatures."""
    with pytest.raises(ValueError):
        simulated_annealing(
            sample_distance_matrix,
            initial_temperature=0
        )


def test_invalid_minimum_temperature(sample_distance_matrix):
    """Reject minimum temperatures greater than initial temperature."""
    with pytest.raises(ValueError):
        simulated_annealing(
            sample_distance_matrix,
            initial_temperature=100,
            min_temperature=100
        )


def test_non_square_matrix():
    """Reject non-square distance matrices."""
    matrix = np.array([
        [0, 5, 3],
        [5, 0, 4]
    ])

    with pytest.raises(ValueError):
        simulated_annealing(matrix)


def test_negative_distances():
    """Reject negative distances."""
    matrix = np.array([
        [0, -5],
        [-5, 0]
    ])

    with pytest.raises(ValueError):
        simulated_annealing(matrix)


def test_non_finite_distances():
    """Reject non-finite distances."""
    matrix = np.array([
        [0, np.inf],
        [np.inf, 0]
    ])

    with pytest.raises(ValueError):
        simulated_annealing(matrix)
