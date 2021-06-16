from os import error
from parser_university import get_author_universities
import json
from json_parser import get_universities_from_json

if __name__ == '__main__':
    get_universities_from_json('./jsons/authors_info.json')