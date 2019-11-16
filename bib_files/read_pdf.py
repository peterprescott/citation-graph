import os
# from tika import parser
# tika requires Java to be installed on your system: https://java.com/en/download/manual.jsp
import re
# import tika
# from tika import unpack
# for some reason to make this work in Windows 7 I had to comment out line 546 in the tika.py file, to stop it throwing an error.
# in my case, this file was here: C:\Users\User\.virtualenvs\citation-graph-IlHssx7R\lib\site-packages\tika\tika.py


# ~ def read_pdf(key):
    # ~ filename = f'{key}_references.pdf'
    # ~ parsed = unpack.from_file(filename)

    # ~ # parsed = parser.from_file(filename)

    # ~ # use regular expressions to pick lines that have a year in brackets in them, then search on Google Scholar...
    # ~ # https://docs.python.org/3/library/re.html

    # ~ with open(f"pdf2txt_{key}.txt", 'w') as file:
        # ~ file.write(parsed['content'])

def extract_references(key):
    extracted_text = ''
    with open(f"pdf2txt_{key}.txt", 'r') as file:
        for line in file:
            extracted_text += line
    # ~ print(extracted_text)
    # ~ \n[\w]+\((19|20)[\d][\d]\)[\w]+\n
    # this could be helpful: https://pythex.org/
    references = re.findall(r"[\n][A-Z].+[,].+[(][\d][\d][\d][\d][)].+", extracted_text)
    for ref in references: print(ref)
    print(len(references))
    # ~ for ref in references: 
        # ~ print(ref.replace('\n',''))
        # ~ print('\n...\n')

        # ~ for line in file:
            # ~ print(re.search(r'*\(\)*',line))

# https://scholar.google.com/scholar?q=
# having extracted the references, we search for them on google scholar.
# why? so that we can then get the citation data
# -- we can use this both to give a citation score,
# and to follow through to the specific citation texts --
# and we can download the pdf of the article (sometimes)
# and extract the reference data from that.
# Also, you can get the doi / isbn,
# and then you can use the zotero/wikipedia api
# to get the clean data for that text in json format
# (just remember to replace the slash with %2f so that the API can understand your URL ).



# ~ read_pdf('RWebberBurrows2018')
# ~ Wyly, E. (2015) 'Gentrification on the Planetary Urban Frontier: The Evolution of Turner's

# there are 210+ refs in RWebberBurrows -- how many can we get?
extract_references('RWebberBurrows2018')


# ~ .replace('','')

