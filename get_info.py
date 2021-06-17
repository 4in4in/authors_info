
from bs4 import BeautifulSoup
import requests
import re

def get_info(link):
    response = requests.get(link)
    try:
        if response.status_code == 200:
            html_doc = response.text
            soup = BeautifulSoup(html_doc, features='html.parser')
            main_tag = soup.find('html')
            content = re.sub(r'\n\s*\n', '\n\n', main_tag.getText().replace('\r',''))
            return content
        else:
            return 'Status code was not 200'
    except:
        return 'Site connection problems'

