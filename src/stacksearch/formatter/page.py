from .question import format_question
from .answer import format_answer

def format_page(question, width):
	question_str = format_question(question, width)
	answers = question.get('answers', [])
	answers.sort(key=lambda x: int(x['score']), reverse=True)
	answer_strs = [format_answer(answer, width) for answer in answers]

	result = "\n\n---\n\n".join([question_str] + answer_strs)
	return result

def main():
	import json
	with open("../test.json", "r") as f:
		data = json.load(f)

	question0 = data['items'][0]
	print(format_page(question0, 140))

if __name__ == "__main__":
	main()
