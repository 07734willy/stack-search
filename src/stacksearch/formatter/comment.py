from html2markdown import convert

from .code import drop_bad_attrs
from .generic import indent, format_date

COMMENT_FORMAT = """
{F_body}
{F_comment_meta}
""".strip()

COMMENT_OWNER_FORMAT = """
    - {creation_date}  |  {F_edited}{display_name} ({reputation})
""".strip()

COMMENT_INDENT = " " * 2

def format_comment_body(body, width):
	new_body = drop_bad_attrs(body)
	text = convert(new_body)
	return indent(text, COMMENT_INDENT, width)

def format_comment_owner(comment):
	creation_date = format_date(comment['creation_date'])
	edited = "[E] " if comment['edited'] else ""
	owner = comment['owner']

	return COMMENT_OWNER_FORMAT.format(
		creation_date=creation_date,
		F_edited=edited,

		display_name=owner['display_name'],
		reputation=owner['reputation'],
	)

def format_comment_meta(comment, width):
	score = comment['score']
	score_str = f"   + {score}  "
	owner_str = format_comment_owner(comment)
	
	padding_size = width - len(score_str) - len(owner_str)
	padding = " " * max(padding_size, 0)

	return f"{score_str}{padding}{owner_str}"
	
def format_comment(comment, width):
	body = format_comment_body(comment['body'], width)
	comment_meta = format_comment_meta(comment, width)
	return COMMENT_FORMAT.format(
		F_body=body,
		score=comment['score'],
		F_comment_meta=comment_meta,
	)

def format_comments(comments, width):
	if not comments:
		return ""
	
	formatted_comments = [format_comment(comment, width) for comment in comments]
	comment_str = "\n\n".join(formatted_comments)
	return f"\n\nComments:\n{comment_str}"
