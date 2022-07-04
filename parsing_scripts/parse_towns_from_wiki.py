import csv

from bs4 import BeautifulSoup

from parsing_scripts.utils import extract_cities_list, load_page

START_PAGE = "https://ru.wikinews.org/wiki/Категория:Населённые_пункты_по_алфавиту"


def main():
    cities = []
    next_page = START_PAGE
    while next_page is not None:
        page = load_page(next_page)
        cities.extend(extract_cities_list(page))
        next_page = link_to_next_page(page)
    with open("../cities-towns.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Город", "Название города", "Страна", "Справка"])
        writer.writerows(cities)


def link_to_next_page(page: BeautifulSoup) -> str:
    links = page.find_all(attrs={"title": "Категория:Населённые пункты по алфавиту"})
    for link in links:
        if link.text.strip() == "Следующая страница":
            return f"https://ru.wikinews.org{link.get('href')}"
    return None


if __name__ == '__main__':
    main()
