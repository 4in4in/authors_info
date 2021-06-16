import json
from os import name
from urllib import parse
import requests
from tqdm import tqdm
import time

from json_parser import get_dict_to_search, save_dict_to_json
from gimg_parser import parse_page
from gecko_driver.driver import Driver

driver = Driver()


def create_query_link(query_string):
    link = f'https://www.google.com/search?q={query_string.replace(" ", "+")}&tbm=isch'
    return link

def search(search_text):
    driver.follow_link(create_query_link(search_text))
    html_data = driver.get_page_source()
    name_url = url.replace('https://','').replace('http://','')
    name_url = name_url[0:name_url.find('/')]
    parse_page(html_data, info['name'], name_url)

if __name__ == '__main__':
    with open('./jsons/authors_infoU4.json', 'r') as f:
        authors_universities = json.load(f)

    dict_to_search = get_dict_to_search(authors_universities)

    for info in dict_to_search:
        if len(info['urls']) > 0:
            for url in [url for url in info['urls'] if url is not None]:
                search_text = info['name'] + ' site:' + url
                search(search_text)
                time.sleep(4)
        else:
            print(info['name'], ': empty urls list')
    
    driver.shutdown()
