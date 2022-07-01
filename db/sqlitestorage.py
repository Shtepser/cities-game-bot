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


init_database()

