
import numpy as np
import pytest

from src.genetic_algorithm import (
    genetic_algorithm,
    order_crossover,
    swap_mutation,
)


@pytest.fixture
def sample_distance_matrix():
    """Create a distance matrix for three cities."""
    return np.array([
        [0, 5, 5],
        [5, 0, np.sqrt(10)],
        [5, np.sqrt(10), 0]
    ])


def test_genetic_algorithm_returns_valid_route(sample_distance_matrix):
    """Check that the algorithm returns a valid route."""
    route, distance, history = genetic_algorithm(
        sample_distance_matrix,
        population_size=20,
        generations=30,
        seed=42
    )

    assert sorted(route.tolist()) == [0, 1, 2]
    assert distance > 0
    assert len(history) == 31


def test_genetic_algorithm_is_reproducible(sample_distance_matrix):
    """Check that identical seeds produce identical results."""
    result1 = genetic_algorithm(
        sample_distance_matrix,
        population_size=20,
        generations=30,
        seed=42
    )

    result2 = genetic_algorithm(
        sample_distance_matrix,
        population_size=20,
        generations=30,
        seed=42
    )

    np.testing.assert_array_equal(result1[0], result2[0])
    assert result1[1] == result2[1]
    assert result1[2] == result2[2]


def test_best_distance_never_increases(sample_distance_matrix):
    """Check that elitism preserves the best distance."""
    _, _, history = genetic_algorithm(
        sample_distance_matrix,
        population_size=20,
        generations=30,
        seed=42
    )

    assert all(
        history[i] <= history[i - 1]
        for i in range(1, len(history))
    )


def test_order_crossover_produces_valid_child():
    """Check that OX produces a valid city permutation."""
    rng = np.random.default_rng(42)

    parent_1 = np.array([0, 1, 2, 3, 4, 5])
    parent_2 = np.array([3, 5, 4, 1, 0, 2])

    child = order_crossover(parent_1, parent_2, rng)

    assert sorted(child.tolist()) == [0, 1, 2, 3, 4, 5]


def test_swap_mutation_preserves_all_cities():
    """Check that mutation preserves city uniqueness."""
    rng = np.random.default_rng(42)

    route = np.array([0, 1, 2, 3, 4, 5])

    mutated = swap_mutation(route, rng)

    assert sorted(mutated.tolist()) == [0, 1, 2, 3, 4, 5]


def test_invalid_population_size(sample_distance_matrix):
    """Reject population sizes below two."""
    with pytest.raises(ValueError):
        genetic_algorithm(
            sample_distance_matrix,
            population_size=1
        )


def test_invalid_generations(sample_distance_matrix):
    """Reject zero or negative generations."""
    with pytest.raises(ValueError):
        genetic_algorithm(
            sample_distance_matrix,
            generations=0
        )


def test_invalid_mutation_rate(sample_distance_matrix):
    """Reject mutation rates outside the valid range."""
    with pytest.raises(ValueError):
        genetic_algorithm(
            sample_distance_matrix,
            mutation_rate=1.5
        )


def test_invalid_crossover_rate(sample_distance_matrix):
    """Reject crossover rates outside the valid range."""
    with pytest.raises(ValueError):
        genetic_algorithm(
            sample_distance_matrix,
            crossover_rate=-0.1
        )


def test_invalid_tournament_size(sample_distance_matrix):
    """Reject tournament sizes larger than the population."""
    with pytest.raises(ValueError):
        genetic_algorithm(
            sample_distance_matrix,
            population_size=10,
            tournament_size=11
        )


def test_non_square_distance_matrix():
    """Reject non-square distance matrices."""
    matrix = np.array([
        [0, 5, 3],
        [5, 0, 4]
    ])

    with pytest.raises(ValueError):
        genetic_algorithm(matrix)


def test_negative_distances():
    """Reject negative distances."""
    matrix = np.array([
        [0, -5],
        [-5, 0]
    ])

    with pytest.raises(ValueError):
        genetic_algorithm(matrix)


def test_single_city_matrix():
    """Reject matrices with fewer than two cities."""
    with pytest.raises(ValueError):
        genetic_algorithm(np.array([[0.0]]))
