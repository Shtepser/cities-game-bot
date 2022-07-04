import csv
import os

from db import add_turns, get_turns, reset_game
from cities_game import handle_turn, TurnResult
from messages import *


def main():
    cities = load_cities()
    id_ = ask_id()
    turns = get_turns(id_)
    turn = input("Ваш ход: ")
    if turn == "Сдаюсь":
        reset_game(id_)
        return
    result, ai_turn = handle_turn(turn, cities, turns)
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
    with open(os.path.join("static", "cities.csv"), encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        return [city for _, city, *_ in reader]


def ask_id() -> int:
    while True:
        try:
            return int(input("Ваш id: "))
        except ValueError:
            print("Введён некорректный id!")


if __name__ == "__main__":
    main()

