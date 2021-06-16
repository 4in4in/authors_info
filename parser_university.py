from os import error
import requests
from googlesearch import search
import time

def get_author_raw_data(scopus_id):
    headers = {'Accept':'application/json', 'X-ELS-APIKey': '35179f93ddd439953a50c9d282ef5eb5'}
    request = requests.get(f'https://api.elsevier.com/content/author/author_id/{scopus_id}', headers=headers)
    return request.json()

def get_author_universities(raw_json):

    scopus_id = raw_json['coredata']['dc:identifier']
    profile = raw_json['author-profile']

    if ('surname' in profile['preferred-name'].keys() and profile['preferred-name']['surname']!=None)\
         and ('given-name' in profile['preferred-name'].keys() and profile['preferred-name']['given-name']!=None):
        name = profile['preferred-name']['surname']+ ' '+ profile['preferred-name']['given-name']
    else:
        name = profile['preferred-name']['indexed-name']

    if 'affiliation-current' in profile and 'affiliation' in profile['affiliation-current']:
        affiliation_current = profile['affiliation-current']['affiliation']
        curr_university_info = get_universities(affiliation_current)
    else:
        curr_university_info = 'no data found'

    if 'affiliation-history' in profile and 'affiliation' in profile['affiliation-history']:
        affiliation_history = profile['affiliation-history']['affiliation']
        university_history_info = get_universities(affiliation_history)
    else:
        university_history_info = 'no data found'

    return { 'scopus_id': scopus_id, 'name': name, 'current_university_info': curr_university_info, 'university_history_info': university_history_info }

def get_university_info(affiliation):
    university = affiliation['ip-doc']
    name = university['afdispname'] if 'afdispname' in university else 'Name not found'
    # url = university['org-URL'] if 'org-URL' in university else None
    # try:
    site_addr = get_university_site(name)
    # except:
    #     site_addr = None
    url = university['org-URL'] if 'org-URL' in university else site_addr
    university_info = { 'name': name, 'url': url }
    return university_info

def get_universities(affiliation_object):
    universities = []
    if isinstance(affiliation_object, dict):
        universities.append(get_university_info(affiliation_object))
    elif isinstance(affiliation_object, list):
        for affiliation in affiliation_object:
            universities.append(get_university_info(affiliation))
    return universities
    

def get_university_site(university_name):
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
    result = search(university_name, num=1, stop=1, pause=5, user_agent=user_agent)
    return list(result)[0]

