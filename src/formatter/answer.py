from generic import format_date, format_last_edited_date
from comment import format_comments
from code import format_body

ANSWER_FORMAT = """
Score: {score}{F_accepted}
Created: {creation_date}{F_last_edited}
By: {display_name} ({reputation})

{F_body}{F_comments}
""".strip()

def format_is_accepted(answer):
	return "  (Accepted)" if answer['is_accepted'] else ""
	
def format_answer(answer, width):
	is_accepted = format_is_accepted(answer)
	creation_date = format_date(answer['creation_date'])
	last_edited_date = format_last_edited_date(answer)
	owner = answer['owner']

	body = format_body(answer['body'], width)
	comments = format_comments(answer.get('comments', []), width)

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
