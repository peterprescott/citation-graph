import os
from tika import parser
import re


def read_pdf(key):
	filename = f'{key}_references.pdf'
	parsed = parser.from_file(filename)
	
	# use regular expressions to pick lines that have a year in brackets in them, then search on Google Scholar...
	# https://docs.python.org/3/library/re.html
		
	with open(f"pdf2txt_{key}.txt", 'w') as file:
		file.write(parsed['content'])
		
	with open(f"pdf2txt_{key}.txt", 'r') as file:
		for line in file:
			print(re.search(r'*\(\)*',line))
	
read_pdf('RWebberBurrows2018')


# ~ .replace('','')
