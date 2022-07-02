import os

from zipfile import ZipFile
from invoke import task


LOCAL_SQLite3_DB = "turns.db"
LOCAL_YDB_DOCKER_PORT = 2136
LOCAL_YDB_DATABASE = "/local"

SOURCES_ARCHIVE = "source.zip"
STATIC_ARCHIVE = "static.zip"


@task
def run_cli(context, db="sqlite"):
    if db == "sqlite":
        _setup_sqlite3_db(context)
    elif db == "ydb-docker":
        _setup_ydb_in_docker(context)
    else:
        raise Exception(f"Unknown --db option: {db}")
    context.run("python3 cli-interface.py")


@task
def bundle(context):
    context.run(f"zip {SOURCES_ARCHIVE} -r requirements.txt LICENSE "
                f"cli_interface.py serverless_interface.py messages.py "
                f"cities_game db telebot_bot "
                f"-x *.pyc -x **/__pycache__/")
    context.run(f"cd static && "
                f"zip ../{STATIC_ARCHIVE} -r .")


def _setup_ydb_in_docker(context):
    os.environ["DB_ENGINE"] = "YDB"
    os.environ["YDB_ENDPOINT"] = f"grpc://localhost:{LOCAL_YDB_DOCKER_PORT}"
    os.environ["YDB_DATABASE"] = LOCAL_YDB_DATABASE
    os.environ["YDB_ANONYMOUS_CREDENTIALS"] = '1'


def _setup_sqlite3_db(context):
    os.environ["DB_ENGINE"] = "SQLite3"
    os.environ["SQLite3_DB_FILE"] = LOCAL_SQLite3_DB

