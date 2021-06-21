
import requests
import asyncio

def get_author_info(scopus_id):
    headers = {'Accept':'application/json', 'X-ELS-APIKey': '35179f93ddd439953a50c9d282ef5eb5'}
    request = requests.get(f'https://api.elsevier.com/content/author/author_id/{scopus_id}', headers=headers)
    return request.json()

async def main():
    id = 56681997900
    loop = asyncio.get_event_loop()
    future1 = loop.run_in_executor(None, get_author_info, id)
    response1 = await future1
    print(response1)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())