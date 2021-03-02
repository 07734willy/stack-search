from argparse import ArgumentParser
from shutil import get_terminal_size

from fetch import search_question
from formatter import format_page


def main():
	width = get_terminal_size((80, 20)).columns

	parser = ArgumentParser()
	parser.add_argument('-i', '--index', type=int, default=0,
		help="Index of result to be returned")
	parser.add_argument('-w', '--width', type=int, default=width,
		help="Explicit width of the formatted output")
	parser.add_argument('-s', '--site', default="stackoverflow.com",
		help="StackExchange site to search")
	parser.add_argument('-b', '--batch-size', dest='batch_size', default=5,
		help="Number of relevent questions to prefetch together")
	parser.add_argument('query',
		help="Query to search")

	args = parser.parse_args()
	question = search_question(args.query, args.site, args.index, args.batch_size)
	result = format_page(question, args.width)

	print(result)
	
if __name__ == "__main__":
	main()
