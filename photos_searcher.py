import json
from os import name
from urllib import parse
import requests
from tqdm import tqdm
import time

from json_parser import get_dict_to_search, save_dict_to_json
from gimg_parser import parse_page
from gecko_driver.driver import Driver

def create_query_link(query_string):
    link = f'https://www.google.com/search?q={query_string.replace(" ", "+")}&tbm=isch'
    return link

if __name__ == '__main__':
    with open('./jsons/authors_infoU4.json', 'r') as f:
        authors_universities = json.load(f)

    dict_to_search = get_dict_to_search(authors_universities)

    # with open('./jsons/search_test2.json', 'r') as f:
    #     dict_to_search = json.load(f)

    driver = Driver()

    for info in dict_to_search:
        if len(info['urls']) > 0:
            for url in info['urls']:
                search_text = info['name'] + ' site:' + url
                driver.follow_link(create_query_link(search_text))
                html_data = driver.get_page_source()
                name_url = url.replace('https://','').replace('http://','')
                name_url = name_url[0:name_url.find('/')]
                parse_page(html_data, info['name'], name_url)
                time.sleep(4)
        else:
            print(info['name'], ': empty urls list')
    
    driver.shutdown()
