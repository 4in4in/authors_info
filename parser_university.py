from os import error
import requests
from ddg1 import DDGSearch

class ParserUniversity:
    @classmethod
    def get_author_universities(cls, raw_json):

        scopus_id = raw_json['coredata']['dc:identifier']
        profile = raw_json['author-profile']

        if ('surname' in profile['preferred-name'].keys() and profile['preferred-name']['surname']!=None)\
            and ('given-name' in profile['preferred-name'].keys() and profile['preferred-name']['given-name']!=None):
            name = profile['preferred-name']['surname']+ ' '+ profile['preferred-name']['given-name']
        else:
            name = profile['preferred-name']['indexed-name']

        if 'affiliation-current' in profile and 'affiliation' in profile['affiliation-current']:
            affiliation_current = profile['affiliation-current']['affiliation']
            curr_university_info = cls.get_universities(affiliation_current)
        else:
            curr_university_info = 'no data found'

        if 'affiliation-history' in profile and 'affiliation' in profile['affiliation-history']:
            affiliation_history = profile['affiliation-history']['affiliation']
            university_history_info = cls.get_universities(affiliation_history)
        else:
            university_history_info = 'no data found'

        return { 'scopus_id': scopus_id, 'name': name, 'current_university_info': curr_university_info, 'university_history_info': university_history_info }

    @classmethod
    def get_university_info(cls, affiliation):
        university = affiliation['ip-doc']
        name = university['afdispname'] if 'afdispname' in university else 'Name not found'
        url = university['org-URL'] if 'org-URL' in university else DDGSearch.ddg_search_with_delay(name)[0]
        university_info = { 'name': name, 'url': url }
        return university_info

    @classmethod
    def get_universities(cls, affiliation_object):
        universities = []
        if isinstance(affiliation_object, dict):
            universities.append(cls.get_university_info(affiliation_object))
        elif isinstance(affiliation_object, list):
            for affiliation in affiliation_object:
                universities.append(cls.get_university_info(affiliation))
        return universities


