from urllib.parse import quote
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

URL_TEMPLATE = 'https://{region}.craigslist.org/search/sss?query={query}'


@dataclass
class Item:
    title: str | None
    link: str | None
    price: str | None
    area: str | None

    _getters = {
        'title': lambda x: x.find('a', {'class': 'result-title'}).text.strip(),
        'link': lambda x: x.find(class_='result-title')['href'].strip(),
        'price': lambda x: x.find(class_='result-price').text.strip(),
        'area': lambda x: x.find(class_='result-hood').text.strip(),
    }

    def __str__(self) -> str:
        return f'{self.title}: {self.price} -- {self.area} ({self.link})'



def scrape(region: str, query: str) -> list[Item]:
    '''
    Search Craigslist for a specific term.
    '''
    # `query` may not be url-safe, due to spaces, etc.
    query = quote(query)
    url = URL_TEMPLATE.format(region=region, query=query)
    response = requests.get(url)
    items = items_from_page(response.content)
    return items


def items_from_page(html: str) -> list[Item]:
    soup = BeautifulSoup(html, features='html.parser')
    raw_items = soup.find_all('li', {'class': 'result-row'})
    items = [item_from_raw(i) for i in raw_items]
    return items


def item_from_raw(raw: Tag) -> Item:
    result_dict = {}
    for field, getter in Item._getters.items():
        try:
            r = getter(raw)
        except Exception:
            print(f'Failed fetching field "{field}" on this entry')
            r = None
        result_dict[field] = r
    return Item(**result_dict)
