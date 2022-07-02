import os
import uuid
import ydb

from datetime import datetime
from typing import List
from ydb import Column, OptionalType, PrimitiveType


DB_ENDPOINT = os.getenv("YDB_ENDPOINT")
DB_DATABASE = os.getenv("YDB_DATABASE")
if DB_ENDPOINT is None or DB_DATABASE is None:
    raise Exception("Wrong configuration: YDB_ENDPOINT and YDB_DATABASE"
                    " environment variables must be set")

DATETIME_FORMAT = "%Y-%m-dT:%H:%M:%SZ"

driver = ydb.Driver(endpoint=DB_ENDPOINT, database=DB_DATABASE)
driver.wait(fail_fast=True, timeout=10)
session = driver.table_client.session().create()


def init_database():
    session.create_table(
        os.path.join(DB_DATABASE, "turns"),
        ydb.TableDescription()
        .with_column(Column("uuid1", OptionalType(PrimitiveType.String)))
        .with_column(Column("stamp", OptionalType(PrimitiveType.Datetime)))
        .with_column(Column("ID_in_transaction", OptionalType(PrimitiveType.Uint8)))
        .with_column(Column("player_id", OptionalType(PrimitiveType.Uint64)))
        .with_column(Column("turn", OptionalType(PrimitiveType.Utf8)))
        .with_primary_key("uuid1")
    )


init_database()


insertion_query = session.prepare("""
        PRAGMA TablePathPrefix("{}");
        DECLARE $UUID AS String;
        DECLARE $stamp AS Datetime;
        DECLARE $ID_in_transaction AS Uint8;
        DECLARE $playerID AS Uint64;
        DECLARE $turn AS Utf8;
        REPLACE INTO turns (uuid1, stamp, ID_in_transaction, player_id, turn) VALUES
        ($UUID, $stamp, $ID_in_transaction, $playerID, $turn);
    """.format(DB_DATABASE))

selection_query = session.prepare("""
        PRAGMA TablePathPrefix("{}");
        DECLARE $playerID AS Uint64;
        SELECT turn, stamp, ID_in_transaction
        FROM turns
        WHERE player_id = $playerID
        ORDER BY stamp, ID_in_transaction;
    """.format(DB_DATABASE))


deletion_query = session.prepare("""
        PRAGMA TablePathPrefix("{}");
        DECLARE $playerID AS Uint64;
        DELETE FROM turns
        WHERE player_id = $playerID;
    """.format(DB_DATABASE))


def add_turns(player_id: int, turns: List[str]):
    for ix, turn in enumerate(turns):
        session.transaction(ydb.SerializableReadWrite()).execute(
            insertion_query, {
                "$UUID": uuid.uuid1().bytes,
                "$stamp": int(datetime.now().timestamp()),
                "$ID_in_transaction": ix,
                "$playerID": player_id,
                "$turn": turn
            },
            commit_tx=True
        )


def get_turns(player_id: int) -> List[str]:
    records = session.transaction(ydb.SerializableReadWrite()).execute(
        selection_query, {
            "$playerID": player_id,
        },
        commit_tx=True
    )[0].rows
    return [record.turn for record in records]


def reset_game(player_id: int):
    session.transaction(ydb.SerializableReadWrite()).execute(
        deletion_query, {
            "$playerID": player_id,
        },
        commit_tx=True
    )

