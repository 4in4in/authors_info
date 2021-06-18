import json
from os import name
from urllib import parse
import requests
from tqdm import tqdm
import time
import random
from datetime import date, datetime

from json_parser import get_dict_to_search, save_dict_to_json
from gimg_parser import parse_page
from gecko_driver.driver import Driver

driver = Driver()


def create_query_link(query_string):
    link = f'https://www.google.com/search?q={query_string.replace(" ", "+")}&tbm=isch'
    return link

def search(search_text, url):
    driver.follow_link(create_query_link(search_text))
    html_data = driver.get_page_source()
    name_url = url.replace('https://','').replace('http://','')
    name_url = name_url[0:name_url.find('/')]
    parse_page(html_data, info['name'], name_url)

if __name__ == '__main__':
    print('start: '+str(datetime.now()))

    with open('./jsons/authors_info_69.json', 'r') as f:
        authors_universities = json.load(f)

    list_to_search = get_dict_to_search(authors_universities)

    print(f'Authors total: {len(list_to_search)}')

    for i in range(len(list_to_search)):
        info = list_to_search[i]

        print(f'Current author: { i + 1 } / { len(list_to_search) } { info["name"]} ')

        if len(urls:=[url for url in info['urls'] if url is not None]) > 0:
            for j in range(len(urls)):
                print(f'Searching site: { j+1 } / { len(urls) } { urls[j] }')

                search_text = info['name'] + ' site:' + urls[j]
                search(search_text, urls[j])
                time.sleep(random.uniform(2.0, 5.0))
        else:
            print(info['name'], ': empty urls list')
    
    driver.shutdown()
    print('end: '+str(datetime.now()))
