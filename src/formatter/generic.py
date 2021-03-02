from textwrap import TextWrapper
from datetime import datetime
import re

LAST_EDITED_DATE_FORMAT = """
  Last Edited: {last_edited_date}
""".strip()

class Wrapper(TextWrapper):
	width = 80
	expand_tabs = False
	tabsize = 4
	replace_whitespace = False
	drop_whitespace = False
	break_long_words = False
	break_on_hyphens = False

def safe_wrap(wrapper, line):
	if re.match(r"^\s*$", line):
		return [wrapper.initial_indent + line] # BUG: can overflow
	return wrapper.wrap(line)

def indent(text, prefix, width=None):
	wrapper = Wrapper()
	wrapper.initial_indent    = prefix
	wrapper.subsequent_indent = prefix
	if width:
		wrapper.width = width

	lines = text.split("\n")
	result = "\n".join(l for ls in lines for l in safe_wrap(wrapper, ls))
	return result

def wrap(text, width=None):
	return indent(text, "", width)

def format_date(epoch_ts):
	date = datetime.fromtimestamp(int(epoch_ts))
	return date.strftime("%b %d '%y at %H:%M")

def format_last_edited_date(item):
	if 'last_edited_date' in item:
		return format_date(item['last_edited_date'])
	return ""
