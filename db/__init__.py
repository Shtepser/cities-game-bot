"""Game status information storage"""
import os
import logging
logger = logging.getLogger("db-loader")
logger.setLevel(logging.INFO)


DB_ENGINE = os.getenv("DB_ENGINE")
if DB_ENGINE is None:
    raise Exception("Wrong configuration: DB_ENGINE environment variable must be set")
if DB_ENGINE == "SQLite3":
    logger.critical("Loading SQLite3 storage")
    from db.sqlitestorage import add_turns, get_turns, reset_game
elif DB_ENGINE == "YDB":
    logger.critical("Loading ydb storage")
    from db.ydbstorage import add_turns, get_turns, reset_game
else:
    raise Exception("Wrong configuration: DB_ENGINE must be of {\"YDB\", \"SQLite3\"}")


__all__ = ["add_turns", "get_turns", "reset_game"]

