from os import stat
import requests
from urllib.parse import urlencode

from bs4 import BeautifulSoup
import time

class DDGSearch:
    headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0', }

    @classmethod
    def __create_link(cls, search_str):
        params = { 'q': search_str }
        link = f'https://duckduckgo.com/html/?{ urlencode(params) }'
        return link

    @classmethod
    def ddg_search(cls, query):
        link = cls.__create_link(query)
        try:
            response = requests.get(link, headers=cls.headers)
        except:
            print('request error')
        else:
            html_doc = response.text
            soup = BeautifulSoup(html_doc, 'html.parser').find_all('a', class_='result__url', href=True)
            links = [ link['href'] for link in soup if 'duckduckgo.com' not in link['href'] ]
            return links

    @classmethod
    def ddg_search_with_delay(cls, query):
        time.sleep(0.001)
        return cls.ddg_search(query)

if __name__ == '__main__':
    # results = DDGSearch.ddg_search('васек трубачев')
    for i in range(100):
        results = DDGSearch.ddg_search_with_delay('Eli Lilly Research Laboratories')[0]
        print(results)
