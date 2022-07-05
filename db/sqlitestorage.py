import os
import sqlite3

from typing import List


DB_FILE = os.getenv("SQLite3_DB_FILE", "turns.db")


def init_database():
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS turns (
                id INTEGER PRIMARY KEY NOT NULL,
                player_id INTEGER NOT NULL,
                turn CHAR[255] NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS difficulty (
                player_id INTEGER PRIMARY KEY NOT NULL,
                level INTEGER NOT NULL
            );
        """)
        connection.commit()


def add_turns(player_id: int, turns: List[str]):
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.executemany("""
            INSERT INTO turns (player_id, turn)
            VALUES (?, ?);
        """,
        [(player_id, turn) for turn in turns])
        connection.commit()


def get_turns(player_id: int) -> List[str]:
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        records = cursor.execute("""
            SELECT turn FROM turns
            WHERE player_id = ?
            ORDER BY id;
        """, (player_id,)).fetchall()
    return [turn for (turn,) in records]


def reset_game(player_id: int):
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM turns WHERE player_id = ?;
        """, (player_id,))
        connection.commit()


def get_difficulty_level(player_id: int) -> int:
    if not _is_difficulty_set(player_id):
        return 0
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        record = cursor.execute("""
            SELECT level FROM difficulty
            WHERE player_id = ?
            LIMIT 1;
        """, (player_id,)).fetchone()
    return record[0]


def set_difficulty_level(player_id: int, level: int):
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        if _is_difficulty_set(player_id):
            request = """
                UPDATE difficulty SET level = :level
                WHERE player_id = :player_id;
            """
        else:
            request = """
                INSERT INTO difficulty (player_id, level)
                VALUES (:player_id, :level);
            """
        cursor.execute(request, {"level": level, "player_id": player_id})
        connection.commit()


def _is_difficulty_set(player_id: int) -> bool:
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        count = cursor.execute("""
            SELECT COUNT(*) FROM difficulty
            WHERE player_id = ?;
        """, (player_id,)).fetchone()[0]
        return bool(count)


init_database()

