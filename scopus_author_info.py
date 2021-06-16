
import requests

def get_author_info(scopus_id):
    headers = {'Accept':'application/json', 'X-ELS-APIKey': '35179f93ddd439953a50c9d282ef5eb5'}
    request = requests.get(f'https://api.elsevier.com/content/author/author_id/{scopus_id}', headers=headers)
    return request.json()