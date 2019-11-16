import os
# from tika import parser
# tika requires Java to be installed on your system: https://java.com/en/download/manual.jsp
import re
# import tika
from tika import unpack
# for some reason to make this work in Windows 7 I had to comment out line 546 in the tika.py file, to stop it throwing an error.
# in my case, this file was here: C:\Users\User\.virtualenvs\citation-graph-IlHssx7R\lib\site-packages\tika\tika.py
import codecs
import requests
import bs4

def read_pdf(key):
    filename = f'{key}.pdf'
    parsed = unpack.from_file(filename)

    # ~ # parsed = parser.from_file(filename)

    # ~ # use regular expressions to pick lines that have a year in brackets in them, then search on Google Scholar...
    # ~ # https://docs.python.org/3/library/re.html
    print(parsed['content'])
    with codecs.open(f"pdf2txt_{key}.txt", 'w', "utf-8") as file:
        file.write(parsed['content'])

def extract_references(key):
    extracted_text = ''
    with codecs.open(f"pdf2txt_{key}.txt", 'r', "utf-8") as file:
        for line in file:
            extracted_text += line
    # ~ print(extracted_text)
    # ~ \n[\w]+\((19|20)[\d][\d]\)[\w]+\n
    # this could be helpful: https://pythex.org/
    references = re.findall(r"[\n][A-Z].+[(][\d][\d][\d][\d][)].+", extracted_text)
    with codecs.open(f"{key}_refs.txt", 'w', "utf-8") as file:
        for ref in references:
            file.write(ref)
            file.write('\n')
            print(ref)
            scrape_scholar(ref)
    print(len(references))
    # ~ for ref in references: 
        # ~ print(ref.replace('\n',''))
        # ~ print('\n...\n')

        # ~ for line in file:
            # ~ print(re.search(r'*\(\)*',line))

def scrape_scholar(reference):
    scraped_page = requests.get(f'https://scholar.google.com/scholar?q={reference}')
    content = scraped_page.text
    citation_score = re.findall(r"Cited by [\d]+", content)
    try:
        print(citation_score[0])
    except:
        pass

    # use bs4 (https://www.crummy.com/software/BeautifulSoup/bs4/doc/) ...
    # to parse the page
    # ~ soup = bs4.BeautifulSoup(content, 'html.parser')
    




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

# ~ read_pdf('EWily2015')
# ~ extract_references('EWily2015')

# ~ scrape_scholar("Teilhard de Chardin P (1964) The Future of Man.")

# ~ .replace('','')

