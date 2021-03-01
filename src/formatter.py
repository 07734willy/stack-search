from textwrap import TextWrapper
from datetime import datetime

from bs4 import BeautifulSoup
from html2markdown import convert

CLOSED_FORMAT = """
Closed: {reason}  Date: {close_date}
""".strip()

LAST_EDITED_DATE_FORMAT = """
  Last Edited: {last_edited_date}
""".strip()

QUESTION_FORMAT = """
# {title}
{F_closed_status}
Score: {score}  Views: {view_count}
Created: {creation_date}{F_last_edited}
By: {display_name} ({reputation})
Tags: {tags}

{F_body}{F_comments}
""".strip()

COMMENT_FORMAT = """
{F_body}
    - {creation_date}   {F_edited}{display_name} ({reputation})
""".strip()

ANSWER_FORMAT = """
Score: {score}{F_accepted}
Created: {creation_date}{F_last_edited}
By: {display_name} ({reputation})

{F_body}{F_comments}
""".strip()

def format_tags(tags):
	return ", ".join(tags)

class Wrapper(TextWrapper):
	width = 80
	expand_tabs = False
	tabsize = 4
	replace_whitespace = False
	drop_whitespace = False
	break_long_words = False
	break_on_hyphens = False

def indent(text, size=2):
	wrapper = Wrapper()
	wrapper.initial_indent    = " " * size
	wrapper.subsequent_indent = " " * size
	lines = text.split("\n")

	result = "\n".join(l for ls in lines for l in wrapper.wrap(ls))
	return result

def drop_problematic_attrs(body):
	soup = BeautifulSoup(body, "html.parser")
	for tag in soup.find_all(rel=True):
		del tag['rel']
	return str(soup)

def format_body(body):
	body = drop_problematic_attrs(body)
	text = convert(body)
	return indent(text)

def format_comment_body(body):
	body = drop_problematic_attrs(body)
	text = convert(body)
	return indent(text)

def format_date(epoch_ts):
	date = datetime.fromtimestamp(int(epoch_ts))
	return date.strftime("%b %d '%y at %H:%M")

def format_last_edited_date(item):
	if 'last_edited_date' in item:
		return format_date(item['last_edited_date'])
	return ""

def format_comment(comment):
	body = format_comment_body(comment['body'])
	creation_date = format_date(comment['creation_date'])
	edited = "[E] " if comment['edited'] else ""
	owner = comment['owner']

	return COMMENT_FORMAT.format(
		F_body=body,
		creation_date=creation_date,
		F_edited=edited,

		display_name=owner['display_name'],
		reputation=owner['reputation'],
	)

def format_comments(comments):
	if not comments:
		return ""
	
	formatted_comments = [format_comment(comment) for comment in comments]
	comment_str = "\n".join(formatted_comments)
	return f"\n\n# Comments:\n{comment_str}"

def format_is_accepted(answer):
	return "  (Accepted)" if answer['is_accepted'] else ""
	
def format_answer(answer):
	is_accepted = format_is_accepted(answer)
	creation_date = format_date(answer['creation_date'])
	last_edited_date = format_last_edited_date(answer)
	owner = answer['owner']

	body = format_body(answer['body'])
	comments = format_comments(answer.get('comments', []))

	return ANSWER_FORMAT.format(
		score=answer['score'],
		F_accepted=is_accepted,
		creation_date=creation_date,
		F_last_edited=last_edited_date,

		display_name=owner['display_name'],
		reputation=owner['reputation'],

		F_body=body,
		F_comments=comments,
	)

def format_closed_status(question):
	if 'close_reason' in question:
		return CLOSED_FORMAT.format(
			close_reason=question['close_reason'],
			close_date=question['close_date'],
		)
	return ""

def format_question(question):
	closed_status = format_closed_status(question)
	creation_date = format_date(question['creation_date'])
	last_edited_date = format_last_edited_date(question)
	owner = question['owner']
	tags = format_tags(question.get('tags', []))
	body = format_body(question['body'])
	comments = format_comments(question.get('comments', []))

	return QUESTION_FORMAT.format(
		title=question['title'],
		F_closed_status=closed_status,
		score=question['score'],
		view_count=question['view_count'],
		creation_date=creation_date,
		F_last_edited=last_edited_date,
		display_name=owner['display_name'],
		reputation=owner['reputation'],
		tags=tags,
		F_body=body,
		F_comments=comments,
	)

def format_all(question):
	question_str = format_question(question)
	answer_strs = [format_answer(answer) for answer in question.get('answers', [])]

	result = "\n\n---\n\n".join([question_str] + answer_strs)
	return result

def main():
	import json
	with open("test.json", "r") as f:
		data = json.load(f)

	question0 = data['items'][0]

	print(format_all(question0))

if __name__ == "__main__":
	main()
