import os
from tika import parser
# tika requires Java to be installed on your system: https://java.com/en/download/manual.jsp
import re
import tika
from tika import unpack
# for some reason to make this work in Windows 7 I had to comment out line 546 in the tika.py file, to stop it throwing an error.


def read_pdf(key):
	filename = f'{key}_references.pdf'
	parsed = unpack.from_file(filename)

    # ~ parsed = parser.from_file(filename)
	
	# use regular expressions to pick lines that have a year in brackets in them, then search on Google Scholar...
	# https://docs.python.org/3/library/re.html
		
	with open(f"pdf2txt_{key}.txt", 'w') as file:
		file.write(parsed['content'])
		
	# ~ with open(f"pdf2txt_{key}.txt", 'r') as file:
		# ~ for line in file:
			# ~ print(re.search(r'*\(\)*',line))
	
read_pdf('RWebberBurrows2018')


# ~ .replace('','')

C:\Users\User\.virtualenvs\citation-graph-IlHssx7R\lib\site-packages\tika\tika.py
