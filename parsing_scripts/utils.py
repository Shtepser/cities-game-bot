import re
import urllib.parse
from typing import List

import urllib3
from bs4 import BeautifulSoup


def link_to_wikipedia(link_to_city: str) -> str:
    wikinews_url = f"https://ru.wikinews.org/{link_to_city}"
    wikinews_content = load_page(wikinews_url)
    wikipedia_link = wikinews_content.select_one("#p-wikibase-otherprojects .wb-otherproject-wikipedia a")
    print(f"Extracted wikipedia page {wikipedia_link} for {link_to_city}")
    return urllib.parse.unquote(wikipedia_link.get("href")) if wikipedia_link else None


def get_country(link_to_city: str) -> str:
    print(f"Processing: {link_to_city}")
    if link_to_city is None:
        return None
    wikipedia_page = load_page(link_to_city)
    info_rows = wikipedia_page.select_one("table.infobox")
    if not info_rows:
        return None
    info_rows = info_rows.tbody.select("tr")
    for row in info_rows:
        if row.th and row.th.text.strip().lower() == "страна":
            return remove_bracketed_group(row.td.text.strip())
    return None


def remove_bracketed_group(city: str) -> str:
    return re.sub(r" ?[(\[].*[)\]]", '', city)


def extract_links_to_cities(page: BeautifulSoup) -> List:
    html_items = page.select(".mw-category-group .CategoryTreeItem a")
    return [(link.text, link_to_wikipedia(link.get("href")))
            for link in html_items]


def extract_cities_list(page: BeautifulSoup) -> List:
    cities_and_links = extract_links_to_cities(page)
    return [(city, remove_bracketed_group(city), get_country(link), link)
            for city, link in cities_and_links]


def load_page(url) -> BeautifulSoup:
    content = urllib3.PoolManager().request("GET", url).data
    return BeautifulSoup(content, "html.parser")
