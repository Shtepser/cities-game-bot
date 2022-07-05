import json
import os

from db import add_turns, get_turns, reset_game
from cities_game import handle_turn, TurnResult, Difficulty
from messages import *


def main():
    cities = load_cities()
    id_ = ask_id()
    difficulty = ask_difficulty()
    turns = get_turns(id_)
    turn = input("Ваш ход: ")
    if turn == "Сдаюсь":
        reset_game(id_)
        return
    result, ai_turn = handle_turn(turn, cities, turns, difficulty)
    if result is TurnResult.success:
        print(successful_turn_report(turn, ai_turn))
        add_turns(id_, [turn, ai_turn])
    elif result is TurnResult.player_wins:
        print(player_victory_report(turn))
        reset_game(id_)
    elif result is TurnResult.unmatched_letters:
        print(unmatched_letters_report(turn, turns[-1]))
    elif result is TurnResult.already_taken:
        print(already_taken_report(turn))
    elif result is TurnResult.no_such_city:
        print(unknown_city_report(turn))


def load_cities():
    with open(os.path.join("static", "cities.json"), encoding="utf-8") as f:
        return json.load(f)


def ask_id() -> int:
    while True:
        try:
            return int(input("Ваш id: "))
        except ValueError:
            print("Введён некорректный id!")


def ask_difficulty() -> Difficulty:
    prompt = f"Желаемая сложность (от 1 до {int(max(Difficulty))};" \
             f" 0 — не установлена): "
    while True:
        try:
            return Difficulty(int(input(prompt)))
        except ValueError:
            print("Введена некорректная сложность")


if __name__ == "__main__":
    main()

