import csv
import json
import os

from collections import defaultdict
from zipfile import ZipFile
from invoke import task


LOCAL_SQLite3_DB = "turns.db"
LOCAL_YDB_DOCKER_PORT = 2136
LOCAL_YDB_DATABASE = "/local"

SOURCES_ARCHIVE = "source.zip"


@task
def run_cli(context, db="sqlite"):
    if db == "sqlite":
        _setup_sqlite3_db(context)
    elif db == "ydb-docker":
        _setup_ydb_in_docker(context)
    else:
        raise Exception(f"Unknown --db option: {db}")
    context.run("python3 cli_interface.py")


@task
def run_server(context, db="sqlite"):
    if db == "sqlite":
        _setup_sqlite3_db(context)
    elif db == "ydb-docker":
        _setup_ydb_in_docker(context)
    else:
        raise Exception(f"Unknown --db option: {db}")
    context.run("python3 server_interface.py")


@task
def bundle(context):
    context.run(f"zip {SOURCES_ARCHIVE} -r requirements.txt LICENSE "
                f"cli_interface.py serverless_interface.py messages.py "
                f"cities_game db telebot_bot "
                f"static/cities.json "
                f"-x *.pyc -x **/__pycache__/")


@task
def csv_cities_to_json(context):
    with open(os.path.join("static", "cities.csv"), encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        cities = [row for row in reader]

    cities_dict = defaultdict(dict)

    for city in cities:
        city, city_name, country, region, info, is_contrary = city
        first_letter = city_name[0]
        cities_dict[first_letter][city_name] = [city_name, country, region, info,
                                                is_contrary == "Да"]

    with open(os.path.join("static", "cities.json"), 'w', encoding="utf-8") as f:
        json.dump(cities_dict, f, ensure_ascii=False, indent=4)


def _setup_ydb_in_docker(context):
    os.environ["DB_ENGINE"] = "YDB"
    os.environ["YDB_ENDPOINT"] = f"grpc://localhost:{LOCAL_YDB_DOCKER_PORT}"
    os.environ["YDB_DATABASE"] = LOCAL_YDB_DATABASE
    os.environ["YDB_ANONYMOUS_CREDENTIALS"] = '1'


def _setup_sqlite3_db(context):
    os.environ["DB_ENGINE"] = "SQLite3"
    os.environ["SQLite3_DB_FILE"] = LOCAL_SQLite3_DB

