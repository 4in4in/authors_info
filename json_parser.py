
import json
from parser_university import ParserUniversity
from tqdm import tqdm
import os

class JsonParser:

    jsons_path = './jsons'

    @classmethod
    def get_universities(cls, data): # получение словаря вида { id автора, имя автора, [университеты автора] }
        results = []
        for author_info_dict in tqdm(data):
            universities = ParserUniversity.get_author_universities(author_info_dict)
            results.append(universities)

        return results

    @classmethod
    def get_dict_to_search(cls, mydata): # получение словаря вида { имя автора: url'ы университетов } для поиска
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

    @classmethod
    def save_dict_to_json(cls, dict, file_name):
        with open(f'{ cls.jsons_path }/{ file_name }.json', 'w') as f:
            json.dump(dict, f, indent=4)

    @classmethod
    def get_dict_from_json(cls, file_name):
        with open(file_name, 'r') as f:
            res_dict = json.load(f)
        return res_dict

    @classmethod
    def get_all_jsons(cls):
        jsons_list = [f for f in os.listdir(cls.jsons_path)\
            if (os.path.isfile(os.path.join(cls.jsons_path, f)) and f.endswith('.json'))]
        return jsons_list


if __name__ == '__main__':
    authors_info = JsonParser.get_dict_from_json('./jsons/authors_info.json')
    
    universities_info = JsonParser.get_universities(authors_info[6]['author-retrieval-response-list']['author-retrieval-response'])
    
    JsonParser.save_dict_to_json(universities_info, f'authors_info_{6}')

    # for i in range(20):
    #     universities_info = JsonParser.get_universities(authors_info[i]['author-retrieval-response-list']['author-retrieval-response'])
    #     JsonParser.save_dict_to_json(universities_info, f'authors_info_{i}')
