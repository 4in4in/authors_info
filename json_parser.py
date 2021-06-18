
import json
from parser_university import get_author_universities
from tqdm import tqdm

def get_universities(data): # получение словаря вида { id автора, имя автора, [университеты автора] }
    results = []
    for author_info_dict in tqdm(data):
        universities = get_author_universities(author_info_dict)
        results.append(universities)

    return results

def get_dict_to_search(mydata): # получение словаря вида { имя автора: url'ы университетов } для поиска
    results =[]
    for info in mydata:
        name = info['name']
        urls = []
        for univ_info in info['current_university_info']:
            if isinstance(univ_info, dict):
                if univ_info['url'] not in urls:
                    urls.append(univ_info['url'])

        for univ_info in info['university_history_info']:
            if isinstance(univ_info, dict):
                if univ_info['url'] not in urls:
                    urls.append(univ_info['url'])

        results.append({'name': name, 'urls': urls})
    return results

def save_dict_to_json(dict, file_name):
    with open(f'./jsons/{file_name}.json', 'w') as f:
        json.dump(dict, f, indent=4)

def get_dict_from_json(file_name):
    with open(file_name, 'r') as f:
        res_dict = json.load(f)
    return res_dict

if __name__ == '__main__':
    authors_info = get_dict_from_json('./jsons/authors_info.json')
    universities_info = get_universities(authors_info[128]['author-retrieval-response-list']['author-retrieval-response'])
    save_dict_to_json(universities_info, 'authors_info_128')
