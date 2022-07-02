from cities_game.game import preprocess


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

