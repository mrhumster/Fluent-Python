from pprint import pprint

import aiohttp
import asyncio

url = 'http://127.0.0.1:8000/tessa/api/journal_records/?page=1&cls=Chronos&pk=5'


async def main():
    auth = aiohttp.BasicAuth(login='Khomyakov.AS', password='nXoouK62')
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(url) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            json = await response.json()
            pprint(json)


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
