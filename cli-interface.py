import os

from cities_game import handle_turn, TurnResult


def main():
    cities = load_cities()
    turns = []
    while True:
        turn = input("Ваш ход: ")
        result, ai_turn = handle_turn(turn, cities, turns)
        if result is TurnResult.success:
            print(f"Ход ИИ: {ai_turn}")
            turns.extend([turn, ai_turn])
        elif result is TurnResult.player_wins:
            print("Поздравляем, вы выиграли!")
            break
        elif result is TurnResult.unmatched_letters:
            print("Первая буква вашего города не совпадает с последней буквой"
                  " предыдущего названного")
        elif result is TurnResult.already_taken:
            print(f"Город {turn} уже называли")
        elif result is TurnResult.no_such_city:
            print(f"Нет такого города, как {turn}")


def load_cities():
    with open(os.path.join("static", "cities.txt"), encoding="utf-8") as f:
        return [city.strip() for city in f.readlines()]


if __name__ == "__main__":
    main()

