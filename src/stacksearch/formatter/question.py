from .generic import format_date, format_last_edited_date
from .comment import format_comments
from .code import format_body

CLOSED_FORMAT = """
Closed: {reason}  Date: {close_date}
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

def format_tags(tags):
	return ", ".join(tags)

def format_closed_status(question):
	if 'close_reason' not in question:
		return ""
	return CLOSED_FORMAT.format(
		close_reason=question['close_reason'],
		close_date=question['close_date'],
	)

def format_question(question, width):
	closed_status = format_closed_status(question)
	creation_date = format_date(question['creation_date'])
	last_edited_date = format_last_edited_date(question)
	owner = question['owner']
	tags = format_tags(question.get('tags', []))
	body = format_body(question['body'], width)
	comments = format_comments(question.get('comments', []), width)

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
