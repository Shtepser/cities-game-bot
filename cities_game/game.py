from enum import auto, Enum
from random import choice
from typing import Iterable, Tuple, Dict


class TurnResult(Enum):
    success = auto()
    already_taken = auto()
    unmatched_letters = auto()
    no_such_city = auto()
    player_wins = auto()


def handle_turn(turn: str, cities: Dict, turns_history: list[str]) \
        -> Tuple[TurnResult, str]:
    if turns_history and not letters_match(turns_history[-1], turn):
        return TurnResult.unmatched_letters, None
    if turn in turns_history:
        return TurnResult.already_taken, None
    if turn not in cities[turn[0]].keys():
        return TurnResult.no_such_city, None
    possible_turns = select_possible_turns(turn, cities, turns_history)
    if len(possible_turns) == 0:
        return TurnResult.player_wins, None
    return TurnResult.success, choice(tuple(possible_turns))


def select_possible_turns(turn: str, cities: Dict, turns_history: Iterable[str]):
    cities_at_the_last_letter = set(cities[preprocess(turn)[-1].upper()])
    return cities_at_the_last_letter - set(turns_history) - {turn}


def letters_match(previous_city, next_city):
    return preprocess(previous_city)[-1] == preprocess(next_city)[0]


def preprocess(city):
    return city.lower().rstrip("ыь ")

