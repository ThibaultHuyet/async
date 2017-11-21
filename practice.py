import aiohttp
import asyncio
import async_timeout
import json

from bs4 import BeautifulSoup

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

async def subreddit(session, name):
	"""
	Returns posts
	"""
	url = "https://www.reddit.com/r/{0}/.json".format(name)
	html = await fetch(session, url)
	for post in json.loads(html)['data']['children']:
		yield post['data']['title']


async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'https://www.reddit.com/r/overwatch/.json')
        for post in json.loads(html)['data']['children']:
        	print(post['data']['title'])

async def main2():
	async with aiohttp.ClientSession() as session:
		async for post in subreddit(session, 'overwatch'):
			print(post)

loop = asyncio.get_event_loop()
loop.run_until_complete(main2())
