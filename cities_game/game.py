from enum import auto, Enum
from random import choice
from typing import Iterable, Tuple


class TurnResult(Enum):
    success = auto()
    already_taken = auto()
    unmatched_letters = auto()
    no_such_city = auto()
    player_wins = auto()


def handle_turn(turn: str, cities: Iterable[str], turns_history: list[str]) \
        -> Tuple[TurnResult, str]:
    if turns_history and not letters_match(turns_history[-1], turn):
        return TurnResult.unmatched_letters, None
    if turn in turns_history:
        return TurnResult.already_taken, None
    if turn not in cities:
        return TurnResult.no_such_city, None
    possible_turns = set(cities) - set(turns_history) - {turn}
    possible_turns = {city for city in possible_turns if letters_match(turn, city)}
    if len(possible_turns) == 0:
        return TurnResult.player_wins, None
    return TurnResult.success, choice(tuple(possible_turns))


def letters_match(previous_city, next_city):
    return preprocess(previous_city)[-1] == preprocess(next_city)[0]


def preprocess(city):
    return city.lower().rstrip("ыь ")

