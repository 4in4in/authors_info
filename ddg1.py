import requests
from urllib.parse import urlencode

from bs4 import BeautifulSoup
import time

headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0', }

def create_link(search_str):
    params = { 'q': search_str }
    link = f'https://duckduckgo.com/html/?{ urlencode(params) }'
    return link

def ddg_search(query):
    link = create_link(query)
    try:
        response = requests.get(link, headers=headers)
    except:
        print('request error')
    else:
        html_doc = response.text
        soup = BeautifulSoup(html_doc, 'html.parser').find_all('a', class_='result__url', href=True)
        links = [ link['href'] for link in soup ]
        return links

def ddg_search_with_delay(query):
    time.sleep(0.1)
    return ddg_search(query)

if __name__ == '__main__':
    results = ddg_search('васек трубачев')
    print(results[0])
