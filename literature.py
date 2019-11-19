import os.path
from pybtex.database import parse_file  # for parsing .bib files
import inspect

# ~ def get_citations(key):

    # ~ bib_data = parse_file(os.path.join('bib_files',f'{key}_citations.bib'))
    # ~ return bib_data

# ~ def get_references(key):

    # ~ bib_data = parse_file(os.path.join('bib_files',f'{key}_references.bib'))
    # ~ return bib_data

texts = []
persons = []
citations = []

class Text(object):
	
	def __init__(	self, 
					key='unknown', 
					creators=[{"creator_type":"unknown",
								"surname":"unknown",
								"initial":"unknown"}], 
					publication_year='unknown', 
					title='unknown',
					references = [],
					referals = []):
		
		self.creators = creators
		for creator in creators:
			# ~ Person(creator.surname, creator.initial).works.append(self) # or something...
			pass
		self.publication_year = publication_year
		
		if self.key == 'unknown':
			if len(self.creators) == 1:
				surnames = self.creators[0].surname
			if len(self.creators) == 2:
				surnames = self.creators[0].surname + self.creators[1].surname
			if len(self.creators) > 2:
				surnames = self.creators[0] + "EtAl"
			proposed_key = self.creators[1].initial + surnames + self.publication_year
			if proposed_key in texts: proposed_key += a
			

		self.title = title
	
class Book(Text):
	
	def __init__(	self, 
					key='unknown', 
					creators=[{"creator_type":"unknown",
								"surname":"unknown",
								"initial":"unknown"}], 
					publication_year='unknown', 
					title='unknown',
					publisher = 'unknown',
					location = 'unknown',
					number_of_pages = 'unknown'):
		
		Text.__init__(key, creators, publication_year, title)
		
		self.publisher = publisher
		self.location = location
		self.number_of_pages = number_of_pages

class Chapter(Text):
	def __init__(	self, 
					key='unknown', 
					creators=[{"creator_type":"unknown",
								"surname":"unknown",
								"initial":"unknown"}], 
					publication_year='unknown', 
					title='unknown',
					publisher = 'unknown',
					location = 'unknown',
					pages = 'unknown'
					book_key = 'unknown'
					book_creators = [1,
								{"creator_type":"unknown",
								"surname":"unknown",
								"initial":"unknown"}], 
					book_title = 'unknown',
					book = None)
):
		
		Text.__init__(self, key, creators, publication_year, title)
		self.publisher = publisher
		self.location = location
		self.pages = pages
		if book == None: 
			self.book = Book(book_key, book_creators, publication_year, book_title, publisher, location)
		self.book_key = self.book.key
		self.book_creators = self.book.creators
		self.book_title = self.book.title
		
class Article(Text):
	
	def __init__(	self, 
					key='unknown', 
					creators=[1,
								{"creator_type":"unknown",
								"surname":"unknown",
								"initial":"unknown"}], 
					publication_year='unknown', 
					title='unknown',
					journal = 'unknown',
					volume = 'unknown',
					edition = 'unknown',
					pages = 'unknown'):
		
		Text.__init__(self, key, creators, publication_year, title)
		self.journal = journal
		self.volume = volume
		self.volume.edition = edition
		self.pages = pages
		

class Person(object):
	
	def __init__(self, surname = "unknown", initial = "unknown"):
		
		self.surname = surname
		self.initial = initial
		self.works = []
		
class Author(Person):
	
	def __init__(self, surname = "unknown", initial = "unknown"):
		
		Person.__init__(self, surname, initial)
		self.type = "author"
		
class Editor(Person)

	def __init__(self, surname = "unknown", initial = "unknown"):
		
		Person.__init__(self, surname, initial)
		self.type = "editor"

class Citation(object):
	
	def __init__(self, cited, citing, year_of_citation):
		
		self.cited = cited
		self.citing = citing
		self.year_of_citation = year_of_citation

# ~ class Text(object):
    
    # ~ def __init__(self, key, pybtex_data = None):
        # ~ """
        # ~ Initialize Text.
        
        # ~ Args:
            # ~ key (string): unique Better BibTeX citation key 
                # ~ in form [authForeIni][authEtAl][year].
            # ~ pybtex_data (pybtex.database.Entry): relevant data from .bib file.
        # ~ """
        
        # ~ self.key = key
        # ~ if os.path.exists(os.path.join('bib_files',f'{key}_references.bib')):
            # ~ self.ref_data = True
        # ~ else: self.ref_data = False
        # ~ if os.path.exists(os.path.join('bib_files',f'{key}_citations.bib')):
            # ~ self.cite_data = True
        # ~ else: self.cite_data = False
        # ~ self.references = []
        # ~ self.citations = []
        # ~ self.detailed = False
        # ~ self.pybtex_data = pybtex_data


        # ~ if self.ref_data:
            # ~ self.get_references()
        # ~ if self.cite_data:
            # ~ self.get_citations()
        # ~ if self.pybtex_data:
            # ~ self.get_detail(pybtex_data)
    
    # ~ def __repr__(self):
        # ~ """ """
# ~ ## # ~       return self.key
        # ~ return '\n'+ self.key + ': ' + self.title
    
    # ~ def get_detail(self, pybtex_data=None):
        # ~ if pybtex_data: 
            # ~ self.type = self.pybtex_data.type
            # ~ for field in self.pybtex_data.fields:
                # ~ setattr(self, field, self.pybtex_data.fields[field].replace('}','').replace('{',''))
            # ~ self.detailed = True
        # ~ else:
            # ~ self.get_references()
        
    # ~ def get_references(self):
        
        # ~ if self.references != []:
            # ~ return self.references
        # ~ elif self.ref_data:
            # ~ bib_data = parse_file(os.path.join('bib_files',f'{self.key}_references.bib'))
            # ~ bib_data.entries[self.key]
            # ~ for entry in bib_data.entries:
                # ~ if entry != self.key:
                    # ~ self.references.append(Text(entry, bib_data.entries[entry]))
            # ~ return self.references
        # ~ else:
            # ~ message = 'There are no references!'
            # ~ print(message)
            # ~ return []
        
    # ~ def get_citations(self):

        # ~ if self.citations != []:
            # ~ return self.citations
        # ~ elif self.cite_data:
            # ~ bib_data = parse_file(os.path.join('bib_files',f'{self.key}_citations.bib'))
            # ~ bib_data.entries[self.key]
            # ~ for entry in bib_data.entries:
                # ~ if entry != self.key:
                    # ~ self.references.append(Text(entry, bib_data.entries[entry]))
            # ~ return self.citations
        # ~ else:
            # ~ message = 'There are no citations!'
            # ~ print(message)
            # ~ return []





# ~ class Author(object)

if __name__ == '__main__':
    ## run some simple tests.
    example_key = 'RWebberBurrows2018'
    example_text = Text(example_key)
    e = example_text
    print(type(e), e.key, e.references, e.citations)
    # ~ for ref in e.references:
        # ~ print(type(ref))


# consider standard API JSON notation for texts and citations...
# [{"itemType":"book","creators":[{"creator_type":"author","firstName":"","lastName":"Timms, Duncan."}],"date":"1971","publisher":"University Press","title":"The urban mosaic : towards a theory of residential differentiation","ISBN":"0521079640, 9780521079648","place":"Cambridge [England]","numPages":"viii, 277 pages","oclc":"132648","url":"https://www.worldcat.org/oclc/132648","accessDate":"2019-11-18"}]
# http://opencitations.net/index/coci/api/v1
# ~ # [
    # ~ {
        # ~ "oci": "02001010806360107050663080702026306630509-0200101080636102704000806",
        # ~ "citing": "10.1186/1756-8722-6-59",
        # ~ "cited": "10.1186/ar4086",
        # ~ "creation": "2013",
        # ~ "timespan": "P1Y",
        # ~ "journal_sc": "no",
        # ~ "author_sc": "no"
    # ~ }
# ~ ]

