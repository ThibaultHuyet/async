import aiohttp
import asyncio
import async_timeout
import json

from bs4 import BeautifulSoup

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

class Subreddit(object):
	"""
	x = Subreddit('chapotraphouse')
	x.subreddit('title', limit = '10')

	>>> post 1
	>>> post 2
	>>> ...
	>>> post 10
	"""
	def __init__(self, sub):
		self.sub = sub

	async def subreddit(self, session, key = 'title', limit = 25):
		url = "https://www.reddit.com/r/{0}/.json?limit={1}".format(self.sub, limit)
		html = await fetch(session, url)
		for post in json.loads(html)['data']['children']:
			yield post['data'][key]

async def main(name, key = 'title', limit = 25):
	s = Subreddit(name)
	async with aiohttp.ClientSession() as session:
		async for post in s.subreddit(session, key, limit):
			print("* " + post)



loop = asyncio.get_event_loop()
loop.run_until_complete(main(name = 'overwatch', limit = 5))