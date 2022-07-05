from math import log2
from random import choices, choice


def easy_ai_choice(possible_turns, distribution):
    weights = [1/log2(i + 2) for i in range(len(distribution))]
    return _choose(possible_turns, distribution, weights)


def hard_ai_choice(possible_turns, distribution):
    weights = [log2(i + 1) for i in range(len(distribution))]
    return _choose(possible_turns, distribution, weights)


def normal_ai_choice(possible_turns, distribution):
    middle = len(distribution) // 2
    weights = [1 / (abs(middle - i) + 1) for i in range(len(distribution))]
    return _choose(possible_turns, distribution, weights)


def random_ai_choice(possible_turns, distribution):
    return choice(tuple(possible_turns))


def _choose(possible_turns, distribution, weights):
    letter = choices([l for l, c in distribution], weights=weights)[0].lower()
    cities_ends_with_letter = tuple(city for city in possible_turns
                                    if city[-1] == letter)
    return choice(cities_ends_with_letter)

