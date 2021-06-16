
# создает json формата id статьи -> id авторов

import json
from parser_university import get_author_universities
from tqdm import tqdm

def get_authors(file_name): # получение словаря формата {"id статьи": [ "id авторов" ]} из файла со списком статей
    result_dict = {}
    with open(file_name, 'r') as f:
        json_data = json.load(f)

    for article_id in json_data:
        authors_list = []
        for author_id in json_data[article_id]:
            authors_list.append(author_id)

        result_dict[article_id] = authors_list

    return result_dict

def get_universities_from_json(file_name): # получение словаря вида { id автора, имя автора, [университеты автора] }
    results = []
    with open(file_name, 'r') as f:
        json_data = json.load(f)

    dicts = json_data[0]['author-retrieval-response-list']['author-retrieval-response']

    for author_info_dict in tqdm(dicts):
        universities = get_author_universities(author_info_dict)
        results.append(universities)

    return results

def get_dict_to_search(mydata): # получение словаря вида { имя автора: url'ы университетов } для поиска
    results =[]
    for info in mydata:
        name = info['name']
        urls = []
        for url in info['current_university_info']:
            if url['url'] not in urls and url['url']:
                urls.append(url['url'])

        for url in info['university_history_info']:
            if url['url'] not in urls and url['url']:
                urls.append(url['url'])

        results.append({'name': name, 'urls': urls})
    return results

def save_dict_to_json(dict, file_name):
    with open(f'./jsons/{file_name}.json', 'w') as f:
        json.dump(dict, f, indent=4)

if __name__ == '__main__':
    universities_info = get_universities_from_json('./jsons/authors_info.json')
    save_dict_to_json(universities_info, 'authors_infoU1')
