from urllib.parse import urlparse
import requests
import re
import os
from json import dump

from websearch import search
from cache import prune_cache, search_cache, update_cache

QUERY_URL = "https://api.stackexchange.com/2.2/questions/{question_ids}?order={order}&sort={sort}&site={site}&filter={filter}"
QUERY_KEY_URL = f"{QUERY_URL}&key={{key}}"

	
def build_url(question_ids, site):
	url = QUERY_URL.format(
		question_ids=';'.join(question_ids),
		order='desc',
		sort='activity',
		site=site,
		filter='!)rTkraPXxg*xgr03n8Uq', # built from https://api.stackexchange.com/docs/questions-by-ids
		#key='AW5L2UbtlbHGP9T5B0KxTg((', # authenticate with key to up quota to 10,000 from 300
	)
	return url

def parse_question_ids(results):
	question_ids = []
	for result in results:
		url_path = urlparse(result.url).path
		match = re.match(r'/questions/(\d+)/', url_path)
		if match:
			question_ids.append(match.group(1))
	return question_ids

def fetch_question_ids(text, site, limit=10):
	results = search(text, site)[:limit]
	question_ids = parse_question_ids(results)
	return question_ids

def fetch_questions(question_ids, site):
	url = build_url(question_ids, site)
	data = requests.get(url).json()
	return data['items']

def search_question(text, site, index=0, batch_size=5):
	question_ids = fetch_question_ids(text, site, max(index+1, batch_size))
	question_id = question_ids[index]

	prune_cache()
	question = search_cache(question_id, site)
	if question:
		return question

	questions = fetch_questions(question_ids, site)
	update_cache(questions, site)

	question = questions[index]
	return question
	

def main():
	question = search_question('how to use functools.partial python', 'stackoverflow.com')
	from .formatter import format_page
	result = format_page(question, 80)
	print(result)

	
if __name__ == "__main__":
	main()
