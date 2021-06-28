
from os import error
from bs4 import BeautifulSoup
import requests
import re
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

class AuthorInfoParser:
    @classmethod
    def get_info(cls, link):
        try:
            response = requests.get(link, timeout=3, verify=False)
        except (HTTPError, ConnectionError, Timeout, RequestException, OSError) as e:
            print(e)
        else:
            if response.status_code == 200:
                if 'pdf' in link:
                    pdf_content = response.content
                    return { 'type': 'pdf', 'content': pdf_content }
                else:
                    html_doc = response.text
                    soup = BeautifulSoup(html_doc, features='html.parser')

                    if main_tag := soup.find('html'):
                        content = re.sub(r'\n\s*\n', '\n\n', main_tag.getText().replace('\r',''))
                        content = link + '\n\n' + content
                        return { 'type': 'text', 'content': content }

                    else:
                        print('not html or pdf')
                        return None
            else:
                print('Status code was not 200')
                return None

if __name__ == '__main__':
    x = AuthorInfoParser.get_info('http://www.sivotecanalytics.com/michael-bergeron.html')
    print(x)