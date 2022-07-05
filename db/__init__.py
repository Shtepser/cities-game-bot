"""Game status information storage"""
import os
import logging
logger = logging.getLogger("db-loader")
logger.setLevel(logging.INFO)

from cities_game import Difficulty


DB_ENGINE = os.getenv("DB_ENGINE")
if DB_ENGINE is None:
    raise Exception("Wrong configuration: DB_ENGINE environment variable must be set")
if DB_ENGINE == "SQLite3":
    logger.critical("Loading SQLite3 storage")
    from db.sqlitestorage import add_turns, get_turns, \
        get_difficulty_level, set_difficulty_level, \
        reset_game
elif DB_ENGINE == "YDB":
    logger.critical("Loading ydb storage")
    from db.ydbstorage import add_turns, get_turns, \
        get_difficulty_level, set_difficulty_level, \
        reset_game
else:
    raise Exception("Wrong configuration: DB_ENGINE must be of {\"YDB\", \"SQLite3\"}")


def get_difficulty(player_id: int) -> Difficulty:
    return Difficulty(get_difficulty_level(player_id))


def set_difficulty(player_id: int, difficulty: Difficulty):
    set_difficulty_level(player_id, int(difficulty))


__all__ = ["add_turns", "get_turns",
           "get_difficulty", "set_difficulty",
           "reset_game"]

