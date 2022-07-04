import csv
import urllib.parse
from typing import List

from bs4 import BeautifulSoup

from parsing_scripts.utils import remove_bracketed_group, load_page

RUSSIAN_CITIES_PAGE = "https://ru.wikipedia.org/wiki/Список_городов_России"


def main():
    page = load_page(RUSSIAN_CITIES_PAGE)
    cities = extract_cities(page)
    save_cities(cities)


def extract_cities(page: BeautifulSoup) -> List:
    cities = []
    tables = page.select("table.standard")
    for table in tables:
        for row in table.tbody.select("tr"):
            if row.text == "":
                continue
            columns = row.select("td")
            if len(columns) == 0:
                continue
            ix, coat, city, region, *_ = columns
            url = urllib.parse.unquote(city.a.get("href"))
            cities.append((city.text, remove_bracketed_group(city.text),
                           region.text,
                           f"https://ru.wikipedia.org{url}"))
    return cities


def save_cities(cities):
    with open("russian-cities.csv", 'w', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Город", "Название города", "Регион", "Справка"])
        writer.writerows(cities)


if __name__ == '__main__':
    main()
