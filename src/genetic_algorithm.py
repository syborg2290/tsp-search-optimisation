
import numpy as np

from src.route_evaluator import calculate_route_distance


def order_crossover(
    parent_1: np.ndarray,
    parent_2: np.ndarray,
    rng: np.random.Generator
) -> np.ndarray:
    """
    Create a child using Order Crossover (OX).

    A segment from parent_1 is preserved. Remaining positions
    are filled using the order of cities in parent_2.
    """
    number_of_cities = len(parent_1)

    if number_of_cities < 2:
        return parent_1.copy()

    start, end = sorted(
        rng.choice(number_of_cities, size=2, replace=False)
    )

    child = np.full(number_of_cities, -1, dtype=int)

    # Preserve a segment from the first parent.
    child[start:end + 1] = parent_1[start:end + 1]

    # Read parent 2 starting immediately after the selected segment.
    remaining_cities = [
        parent_2[(end + 1 + offset) % number_of_cities]
        for offset in range(number_of_cities)
        if parent_2[(end + 1 + offset) % number_of_cities] not in child
    ]

    # Fill empty child positions in circular order.
    empty_positions = [
        (end + 1 + offset) % number_of_cities
        for offset in range(number_of_cities)
        if child[(end + 1 + offset) % number_of_cities] == -1
    ]

    for position, city in zip(empty_positions, remaining_cities):
        child[position] = city

    return child


def swap_mutation(
    route: np.ndarray,
    rng: np.random.Generator
) -> np.ndarray:
    """
    Mutate a route by swapping two randomly selected cities.
    """
    mutated_route = route.copy()

    if len(mutated_route) < 2:
        return mutated_route

    position_1, position_2 = rng.choice(
        len(mutated_route),
        size=2,
        replace=False
    )

    mutated_route[position_1], mutated_route[position_2] = (
        mutated_route[position_2],
        mutated_route[position_1]
    )

    return mutated_route


def tournament_selection(
    population: list[np.ndarray],
    fitness: np.ndarray,
    tournament_size: int,
    rng: np.random.Generator
) -> np.ndarray:
    """
    Select the best candidate from a random tournament.
    """
    selected_indices = rng.choice(
        len(population),
        size=tournament_size,
        replace=False
    )

    winner_index = selected_indices[
        np.argmin(fitness[selected_indices])
    ]

    return population[winner_index].copy()


def genetic_algorithm(
    distance_matrix: np.ndarray,
    population_size: int = 100,
    generations: int = 100,
    crossover_rate: float = 0.9,
    mutation_rate: float = 0.1,
    tournament_size: int = 3,
    seed: int | None = None
) -> tuple[np.ndarray, float, list[float]]:
    """
    Solve the TSP using a Genetic Algorithm.

    Returns:
        Best route, best route distance, and best-distance history.
    """
    distance_matrix = np.asarray(distance_matrix)

    if distance_matrix.ndim != 2:
        raise ValueError("Distance matrix must be two-dimensional.")

    rows, columns = distance_matrix.shape

    if rows < 2 or rows != columns:
        raise ValueError(
            "Distance matrix must be square and contain at least two cities."
        )

    if not np.issubdtype(distance_matrix.dtype, np.number):
        raise ValueError("Distance matrix must contain numeric values.")

    if not np.isfinite(distance_matrix).all():
        raise ValueError("Distance matrix must contain finite values.")

    if np.any(distance_matrix < 0):
        raise ValueError("Distances cannot be negative.")

    integer_parameters = {
        "population_size": population_size,
        "generations": generations,
        "tournament_size": tournament_size
    }

    for name, value in integer_parameters.items():
        if isinstance(value, bool) or not isinstance(
            value, (int, np.integer)
        ):
            raise ValueError(f"{name} must be an integer.")

    if population_size < 2:
        raise ValueError("Population size must be at least 2.")

    if generations <= 0:
        raise ValueError("Generations must be positive.")

    if not 1 <= tournament_size <= population_size:
        raise ValueError(
            "Tournament size must be between 1 and population size."
        )

    if not 0 <= crossover_rate <= 1:
        raise ValueError("Crossover rate must be between 0 and 1.")

    if not 0 <= mutation_rate <= 1:
        raise ValueError("Mutation rate must be between 0 and 1.")

    rng = np.random.default_rng(seed)

    number_of_cities = rows

    # Generate the initial population.
    population = [
        rng.permutation(number_of_cities)
        for _ in range(population_size)
    ]

    # Evaluate the initial population.
    fitness = np.array([
        calculate_route_distance(route, distance_matrix)
        for route in population
    ])

    best_index = int(np.argmin(fitness))
    best_route = population[best_index].copy()
    best_distance = float(fitness[best_index])

    history = [best_distance]

    for _ in range(generations):

        # Generate a new population.
        new_population = []

        # Preserve the best individual (elitism).
        new_population.append(best_route.copy())

        while len(new_population) < population_size:

            # Select two parents.
            parent_1 = tournament_selection(
                population,
                fitness,
                tournament_size,
                rng
            )

            parent_2 = tournament_selection(
                population,
                fitness,
                tournament_size,
                rng
            )

            # Apply crossover.
            if rng.random() < crossover_rate:
                child_1 = order_crossover(parent_1, parent_2, rng)
                child_2 = order_crossover(parent_2, parent_1, rng)
            else:
                child_1 = parent_1.copy()
                child_2 = parent_2.copy()

            # Apply mutation independently.
            if rng.random() < mutation_rate:
                child_1 = swap_mutation(child_1, rng)

            if rng.random() < mutation_rate:
                child_2 = swap_mutation(child_2, rng)

            new_population.append(child_1)

            if len(new_population) < population_size:
                new_population.append(child_2)

        population = new_population

        # Evaluate the new population.
        fitness = np.array([
            calculate_route_distance(route, distance_matrix)
            for route in population
        ])

        # Update the best solution.
        generation_best_index = int(np.argmin(fitness))
        generation_best_distance = float(
            fitness[generation_best_index]
        )

        if generation_best_distance < best_distance:
            best_distance = generation_best_distance
            best_route = population[generation_best_index].copy()

        history.append(best_distance)

    return best_route, best_distance, history
