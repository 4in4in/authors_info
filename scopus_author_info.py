
import requests
from json_parser import JsonParser

class ScopusInfo:
    
    @classmethod
    def get_author_info(cls, scopus_id):
        headers = {'Accept':'application/json', 'X-ELS-APIKey': '35179f93ddd439953a50c9d282ef5eb5'}
        request = requests.get(f'https://api.elsevier.com/content/author/author_id/{scopus_id}', headers=headers)
        info_dict = request.json()
        author_universities = JsonParser.get_universities(info_dict['author-retrieval-response'])
        return author_universities


if __name__ == '__main__':
    id = 57210625799
    author_info = get_author_info(id)
    author_universities = JsonParser.get_universities(author_info['author-retrieval-response'])
    JsonParser.save_dict_to_json(author_universities, str(id))