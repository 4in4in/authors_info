import json
import time
import random
from datetime import  datetime
from urllib.parse import urlencode

from json_parser import JsonParser
from gimg_parser import GoogleImgParser
from gecko_driver.driver import Driver

driver = Driver()

def create_query_link(query_string):
    params = {'q': query_string, 'tbm': 'isch'}
    link = f'https://www.google.com/search?{ urlencode(params) }'
    return link

def search_author(search_text, author_name, url):
    driver.follow_link(create_query_link(search_text))
    html_data = driver.get_page_source()
    name_url = url.replace('https://','').replace('http://','')
    name_url = name_url[0:name_url.find('/')]
    GoogleImgParser.parse_page(html_data, author_name, name_url)

def search_all_authors(list_to_search):
    for i in range(len(list_to_search)):
        info = list_to_search[i]

        print(f'Current author: { i + 1 } / { len(list_to_search) } { info["name"]} ')

        if len(urls:=[url for url in info['urls'] if url is not None]) > 0:
            for j in range(len(urls)):
                print(f'Searching site: { j+1 } / { len(urls) } { urls[j] }')

                search_text = info['name'] + ' site:' + urls[j]
                search_author(search_text, info['name'] ,urls[j])
                time.sleep(random.uniform(2.0, 5.0))
        else:
            print(info['name'], ': empty urls list')
    pass

if __name__ == '__main__':
    start_time = datetime.now()
    print(f'start: {start_time}')

    with open('./jsons/authors_info_85.json', 'r') as f:
        authors_universities = json.load(f)

    list_to_search = JsonParser.get_dict_to_search(authors_universities)

    print(f'Authors total: {len(list_to_search)}')

    search_all_authors(list_to_search)
    
    driver.shutdown()
    end_time = datetime.now()
    print(f'end: {end_time}')
    print(f'total time: { end_time - start_time }')
