from urllib.parse import urlparse
import requests
import re
import os
from json import dump

from websearch import search

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

def fetch_questions(text, site, limit=10):
	results = search(text, site)[:limit]
	question_ids = parse_question_ids(results)
	url = build_url(question_ids, site)

	data = requests.get(url).json()
	return data

def main():
	data = fetch_questions('how to use groupby python', 'stackoverflow.com', 3)
	from pprint import pprint
	pprint(data)
	with open("test.json", "w") as f:
		dump(data, f, indent="    ")

	
if __name__ == "__main__":
	main()
