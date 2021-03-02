from html2markdown import convert
from bs4 import BeautifulSoup

from .generic import indent, wrap

BODY_PREFIX = " " * 2

def drop_bad_attrs(body):
	soup = BeautifulSoup(body, "html.parser")
	for tag in soup.find_all(rel=True):
		del tag['rel']
	for tag in soup.find_all(class_=True):
		del tag['class']
	return str(soup)

def fix_code_blocks(body, width):
	soup = BeautifulSoup(body, "html.parser")
	for pre in soup.find_all("pre"):
		code_block = pre.find("code")
		if code_block:
			code = code_block.string
			code = wrap(code, width-4)
			code_block.string.replace_with(code)
	return str(soup)

def format_body(body, width):
	body = drop_bad_attrs(body)
	body = fix_code_blocks(body, width - len(BODY_PREFIX))
	text = convert(body)
	out = indent(text, BODY_PREFIX, width)
	return out
