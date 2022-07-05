from enum import auto, Enum, IntEnum
from random import choice
from typing import Iterable, Tuple, Dict


class TurnResult(Enum):
    success = auto()
    already_taken = auto()
    unmatched_letters = auto()
    no_such_city = auto()
    player_wins = auto()


class Difficulty(IntEnum):
    not_set = 0
    easy = 1
    normal = 2
    hard = 3


def handle_turn(turn: str, cities: Dict, turns_history: list[str],
                difficulty: Difficulty) -> Tuple[TurnResult, str]:
    if turns_history and not letters_match(turns_history[-1], turn):
        return TurnResult.unmatched_letters, None
    if turn in turns_history:
        return TurnResult.already_taken, None
    if turn not in cities[turn[0]].keys():
        return TurnResult.no_such_city, None
    possible_turns = select_possible_turns(turn, cities, turns_history)
    if len(possible_turns) == 0:
        return TurnResult.player_wins, None
    return TurnResult.success, \
           select_ai_turn(possible_turns, difficulty, cities, turns_history)


def select_possible_turns(turn: str, cities: Dict, turns_history: Iterable[str]):
    cities_at_the_last_letter = set(cities[preprocess(turn)[-1].upper()])
    return cities_at_the_last_letter - set(turns_history) - {turn}


def select_ai_turn(possible_turns, difficulty, cities, turns_history):
    return choice(tuple(possible_turns))


def letters_match(previous_city, next_city):
    return preprocess(previous_city)[-1] == preprocess(next_city)[0]


def preprocess(city):
    return city.lower().rstrip("ыь ")

