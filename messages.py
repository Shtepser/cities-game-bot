from typing import List

from cities_game.game import preprocess, Difficulty


def successful_turn_report(player_turn: str, ai_turn: str) -> str:
    return ai_turn


def player_victory_report(player_turn: str) -> str:
    return "Бот сдался. Вы победили."


def bot_victory_report() -> str:
    return "Вы сдались. Бот победил."


def unmatched_letters_report(player_turn: str, previous_turn: str) -> str:
    return f"{previous_turn} — на «{preprocess(previous_turn)[-1]}», " + \
           f"а {player_turn} — на «{preprocess(player_turn)[0]}»!"


def already_taken_report(player_turn: str) -> str:
    # TODO 
    return "Уже было!"


def unknown_city_report(player_turn: str) -> str:
    return f"Не знаю я город {player_turn}..."


def city_info(city: List, use_markdown=True) -> str:
    city, country, region, info_link, is_contrary = city
    if use_markdown:
        name = f"[{city}]({info_link.replace(')', '%29')})"
    else:
        name = city
    if is_contrary:
        territorial_info = ''
    elif country == "Россия":
        territorial_info = f", {region}"
    else:
        territorial_info = f", {country}"
    return f"Город {name}{territorial_info}."


def difficulty_name(difficulty: Difficulty) -> str:
    return {
        Difficulty.not_set: "не установлена (полная случайность)",
        Difficulty.easy: "низкая",
        Difficulty.normal: "нормальная",
        Difficulty.hard: "высокая"
    }[difficulty]

