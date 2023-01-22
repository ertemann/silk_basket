


def compute_starting_weights(prices: list[float],
                              weights: list[float],
                              target_peg: float) -> list[float]:
    starting_weights = target_peg * weights / prices

    assert sum(prices * starting_weights) == target_peg

    return starting_weights


def update_starting_peg(starting_weights: list[float],
                         prices: list[float]):
    return sum(starting_weights * prices)






