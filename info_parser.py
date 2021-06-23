
from os import error
from bs4 import BeautifulSoup
import requests
import re
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

class AuthorInfoParser:
    @classmethod
    def get_info(cls, link):
        try:
            response = requests.get(link, timeout=3)
        except (HTTPError, ConnectionError, Timeout, RequestException, OSError) as e:
            print(e)
        else:
            if response.status_code == 200:
                html_doc = response.text
                soup = BeautifulSoup(html_doc, features='html.parser')
                main_tag = soup.find('html')
                if main_tag:
                    content = re.sub(r'\n\s*\n', '\n\n', main_tag.getText().replace('\r',''))
                    return content
                else:
                    print('page is not html')
            else:
                print('Status code was not 200')

if __name__ == '__main__':
    x = AuthorInfoParser.get_info('http://www.sivotecanalytics.com/michael-bergeron.html')
    print(x)