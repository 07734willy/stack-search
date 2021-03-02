from datetime import timedelta, datetime, timezone
import shelve
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILENAME = os.path.join(SCRIPT_DIR, "stack.cache")
CACHE_EXPIRY = timedelta(days=2)

def tokey(question_id, site):
	return f"{question_id}-{site}"

def search_cache(question_id, site):
	key = tokey(question_id, site)
	with shelve.open(CACHE_FILENAME) as cache:
		if key in cache:
			question = cache[key]
			return question

def update_cache(questions, site):
	access_date = datetime.now().replace(tzinfo=timezone.utc).timestamp()
	with shelve.open(CACHE_FILENAME) as cache:
		for question in questions:
			key = tokey(question['question_id'], site)
			question['access_date'] = access_date
			cache[key] = question

def prune_cache():
	with shelve.open(CACHE_FILENAME) as cache:
		for key, question in list(cache.items()):
			access_date = datetime.utcfromtimestamp(question['access_date'])
			if access_date + CACHE_EXPIRY < datetime.now():
				del cache[key]
