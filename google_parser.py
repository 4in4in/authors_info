import requests
import time
from random import uniform

from bs4 import BeautifulSoup
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

def create_search_link(query):
    return f'https://www.google.com/search?q={query.replace(" ","+")}'

def search(query):
    try:
        resp = requests.get(create_search_link(query), headers=headers)
    except (HTTPError, ConnectionError, Timeout, RequestException, OSError) as e:
        print(e)
    else:
        if resp.status_code == 200:
            time.sleep(uniform(0.9, 1.6))
            html_doc = resp.text
            soup = BeautifulSoup(html_doc, features='html.parser')
            a_tags = soup.findAll('a')
            if a_tags:
                urls = [url for url in a_tags if \
                    (url.has_attr('data-ved') and url.has_attr('href') and url.has_attr('onmousedown'))]
                urls = [url['href'] for url in urls]
                if urls:
                    return urls[0]

if __name__ == '__main__':
    results = search('onmyo-za')
    print(results[0])