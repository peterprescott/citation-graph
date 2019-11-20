"""
Class frameworks for: Text, Book, Chapter, Article, Person, Author, Editor,	Citation.
"""

import os.path
from pybtex.database import parse_file  # for parsing .bib files
import db_commands as db

# ~ def get_citations(key):

    # ~ bib_data = parse_file(os.path.join('bib_files',f'{key}_citations.bib'))
    # ~ return bib_data

# ~ def get_references(key):

    # ~ bib_data = parse_file(os.path.join('bib_files',f'{key}_references.bib'))
    # ~ return bib_data


class Text(object):
	"""A Text has a 'key' and a 'type'."""
	
	def __init__(	self, 
					key,
					creators=[{"creator_type":"unknown",
								"surname":"unknown",
								"initial":"unknown"}], 
					publication_year='unknown', 
					title='unknown',
					text_type='unknown', 
					references = [],
					referals = []):
		"""Initializes Text object."""
		
		self.creators = creators
		for creator in creators:
			# ~ Person(creator.surname, creator.initial).works.append(self) # or something...
			pass
		self.publication_year = publication_year
		
		self.key = key
		if self.key == 'unknown':
			if len(self.creators) == 1:
				surnames = self.creators[0].surname
			if len(self.creators) == 2:
				surnames = self.creators[0].surname + self.creators[1].surname
			if len(self.creators) > 2:
				surnames = self.creators[0] + "EtAl"
			proposed_key = self.creators[1].initial + surnames + self.publication_year
			if proposed_key in texts: proposed_key += a
			
		self.references = references
		self.referals = referals
		self.title = title
		self.text_type = text_type
		self.save()
		
	def save(self):
		"""Saves Text to SQLite database"""
		
		row = (self.key, self.text_type)
		db.save_row_to_table("texts", row)
	
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
		"""Initialize Book as child Text object."""
		
		Text.__init__(key, creators, publication_year, title, text_type = "book")

		self.publisher = publisher
		self.location = location
		self.number_of_pages = number_of_pages
		self.save()
		
	def save(self):
		"""Saves Book to SQLite database"""
		
		row = (self.key, self.publication_year, self.title, self.publisher, self.location, self.number_of_pages)
		db.save_row_to_table("books", row)

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
					pages = 'unknown',
					book_key = 'unknown',
					book_creators = [1,
								{"creator_type":"unknown",
								"surname":"unknown",
								"initial":"unknown"}],
					book_title = 'unknown'):
		"""Initialize Chapter as child Text object."""
		
		Text.__init__(self, key, creators, publication_year, title, text_type = "chapter")
		self.type = "chapter"
		self.publisher = publisher
		self.location = location
		self.pages = pages
		if book == None: 
			self.book = Book(book_key, book_creators, publication_year, 
										book_title, publisher, location)
		self.book_key = self.book.key
		self.book_creators = self.book.creators
		self.book_title = self.book.title
		self.save()
		
	def save():
		"""Saves chapter to SQLite database."""
		
		row = (self.key, self.title, self.pages, self.book_key)
		db.save_row_to_table("chapters", row)


		
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
					# volume = 'unknown',
					edition = 'unknown',
					pages = 'unknown'):
		"""Initialize Article as child Text object."""
		
		Text.__init__(self, key, creators, publication_year, title, text_type = "article")
		self.journal = journal
		self.volume = volume
		self.volume.edition = edition
		self.pages = pages
		self.save()
		
	def save():
		"""Saves article to SQLite database."""
		  
		row = (self.key, self.publication_year, self.title, self.journal, self.edition, self.pages)
		db.save_row_to_table("articles", row)
		

class Person(object):
	
	def __init__(self, surname = "unknown", initial = "unknown"):
		"""Initialize Person object."""
		
		self.surname = surname
		self.initial = initial
		self.works = []
		self.save()
		
	def save(self):
		# ~ creator_columns = ('key', 'surname', 'initial', 'year_of_birth', 'year_of_death')
		pass
  
		
class Author(Person):
	
	def __init__(self, surname = "unknown", initial = "unknown"):
		
		Person.__init__(self, surname, initial)
		self.type = "author"
		
class Editor(Person):

	def __init__(self, surname = "unknown", initial = "unknown"):
		
		Person.__init__(self, surname, initial)
		self.type = "editor"

class Citation(object):
	
	def __init__(self, citing, cited):
		"""Initialize Citation object."""
		
		self.key = citing+'-->'+cited
		self.citing = citing
		self.cited = cited
		# ~ self.year_of_citation = year_of_citation
		
		self.save()
		
	def save(self):
		"""Saves citation to SQLite database."""
		
				    # ~ text_creator_columns = ('key', 'text_key', 'creator_key', 'creator_type', 'creator_ordinal')
		citation_columns = ('key', 'citing_key', 'cited_key')
		row = (self.key, self.citing, self.cited)
		db.save_row_to_table("citations", row)
		pass

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
    print(type(e), e.key, e.references, e.referals)
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

