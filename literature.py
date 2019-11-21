"""
Class frameworks for: Text, Book, Chapter, Article, Creator, Citation.
"""

import os.path
import sys

import db_commands as db
import reader

class Text(object):
    """A Text has a 'key' and a 'type'."""
    
    text_types = ("book", "chapter", "article")

    
    def __init__(   
                self, db_file, key='?', publication_year='?', title='?', 
                text_type='?', doi='?', references=[], referals=[],
                creators=[{"surname":"?", "initial":"?", "role":"?"}]):
        """Initializes Text instance.
        
        Args:
            db_file (string): file location of database
            key (string): in BetterBibTex format [authForeIni][authEtAl][year].
            publication_year (string): YYYY
            title (string)
            text_type (string)
            references (list): texts cited by this Text.
            referals (list): texts which cite this Text.
            creators (JSON, ie. list of dicts): 
                                specifying 'surname', 'initial' and 'role'."""
        
        self.db_file = db_file
        self.q = db.Query(db_file)
        self.creators = creators
        for creator in creators:
            # ~ Person(creator.surname, creator.initial).works.append(self) # or something...
            pass
        self.publication_year = publication_year
        
        self.key = key
        if self.key == '?':
            if len(self.creators) == 1:
                surnames = self.creators[0]["surname"]
            surnames = '?'
            if len(self.creators) == 2:
                surnames = self.creators[0]["surname"] + self.creators[1]["surname"]
            if len(self.creators) > 2:
                surnames = self.creators[0] + "EtAl"
            proposed_key = self.creators[0]["initial"] + surnames + self.publication_year
            # TODO: add 'a','b','c' etc. to proposed_key if key exists and text is new
            
        self.references = references
        
        self.referals = referals
        self.title = title
        if text_type in self.text_types:
            self.text_type=text_type
        else: 
            print(f"'{text_type}' not recognized as valid text.type")
            self.text_type = '?'
        self.doi = doi
        self.save()
        
    def save(self):
        """Saves Text to SQLite database."""
        
        row = (self.key, self.publication_year, self.title, self.text_type, self.doi)
        print(row)
        self.q.save_row_to_table("texts", row)
        for index, creator in enumerate(self.creators):
            creator["instance"] = Creator(self.db_file, creator["surname"], creator["initial"])
            text_creator_row = (self.key+str(index), self.key, creator["instance"].key, creator["role"], index)
            self.q.save_row_to_table("text_creators", text_creator_row)
        
    def remove(self, all_but=0):
        """Removes Text from SQLite database."""
    
        self.q.remove_duplicate_rows("texts", self.key, all_but=0)
        self.q.remove_duplicate_rows("text_creators", self.key, all_but=0, column="text_key")
        for creator in self.creators:
            # ~ if creator no longer has any texts: delete creator
            creator_exists = self.q.search(
                                        "text_creators", "creator_key", 
                                        creator["initial"]+creator["surname"])
            if not creator_exists:
                self.q.remove_duplicate_rows("creators", self.key, all_but=0)
        if self.text_type in self.text_types:
            self.q.remove_duplicate_rows(self.text_type+"s", self.key, all_but=0)
            
    
class Book(Text):
    
    def __init__(
                self, db_file, key='?', publication_year='?', title='?',
                publisher = '?', location = '?', number_of_pages = '?',
                doi='?', isbn='?', references=[], referals=[], 
                creators=[{"surname":"?", "initial":"?", "role":"?"}]):
        """Initialize Book as child Text instance."""
        
        self.db_file = db_file
        self.publisher = publisher
        self.location = location
        self.number_of_pages = number_of_pages
        self.isbn = isbn

        Text.__init__(
                    self, db_file, key, publication_year, title, "book",
                    doi, references, referals, creators)
        
    def save(self):
        """Saves Book to SQLite database: to 'texts' and 'books' tables."""
        
        Text.save(self)
        row = (self.key, self.publisher, self.location, self.number_of_pages, self.isbn)
        self.q.save_row_to_table("books", row)


class Chapter(Text):
    def __init__(   
                self, db_file, key='?', publication_year='?', title='?',
                    publisher = '?', location = '?', pages = '?', 
                    doi='?', references=[], referals=[],
                    creators=[{"surname":"?", "initial":"?", "role":"?"}],
                    book_key = '?', book_title = '?', book=None,
                    book_creators =[{"surname":"?", "initial":"?", "role":"?"}]):
        """
        Initialize Chapter as child Text instance,
        and (unless supplied) initializes its containing book as Book instance.
        """
        
        self.db_file = db_file
        self.publisher = publisher
        self.location = location
        self.pages = pages
        if book == None: 
            self.book = Book(self.db_file, book_key, publication_year, 
                        book_title, publisher, location, creators=book_creators)
        else:
            self.book = book
        self.book_key = self.book.key
        self.book_creators = self.book.creators
        self.book_title = self.book.title

        Text.__init__(
                        self, db_file, key, publication_year, title, "chapter",
                        doi, references, referals, creators)
        
        
    def save(self):
        """Saves chapter to SQLite database: to 'texts' and 'chapters' tables."""
        
        Text.save(self)
        row = (self.key, self.title, self.pages, self.book_key)
        self.q.save_row_to_table("chapters", row)

    def remove(self, remove_book=True):
        """Removes chapter *and* (by default) book from SQLite database.
        
        Args:
            remove_book (Boolean): if True, also removes book containing chapter."""
            
        Text.remove(self)
        Text.remove(self.book)
        
        
class Article(Text):
    
    def __init__(
                self, db_file, key='?', publication_year='?', title='?',
                journal='?', volume='?', edition='?', pages='?', 
                doi='?', references=[], referals=[], 
                creators=[{"surname":"?", "initial":"?", "role":"?"}]):
        """Initialize Article as child Text instance."""
        
        self.db_file = db_file
        self.journal = journal
        self.volume = volume
        self.edition = edition
        self.pages = pages

        Text.__init__(
                    self, db_file, key, publication_year, title, "article",
                        doi, references, referals, creators)

        
    def save(self):
        """Saves article to SQLite database."""

        Text.save(self)          
        row = (self.key, self.journal, self.volume, self.edition, self.pages)
        self.q.save_row_to_table("articles", row)
        

class Creator(object):
    
    def __init__(self, db_file, surname = "?", initial = "?"):
        """Initialize Creator instance."""
        
        self.db_file = db_file
        self.q = db.Query(db_file)
        self.surname = surname
        self.initial = initial
        self.key = self.initial + self.surname
        self.works = []
        self.save()
        
    def save(self):
        """Save creator to SQLite database."""
        
        row = (self.key, self.surname, self.initial)
        self.q.save_row_to_table("creators", row)
        
    
    def remove(self):
        self.q.remove_duplicate_rows("creators", self.key, all_but=0)
        
        
class Citation(object):
    
    def __init__(self, db_file, citing, cited):
        """
        Initialize Citation instance.
        
        Args:
            citing (string): key of citing text.
            cited (string): key of cited text.
        """
        
        self.db_file = db_file
        self.q = db.Query(db_file)
        self.key = citing+'-->'+cited
        self.citing = citing
        self.cited = cited
        
        self.save()
        
    def save(self):
        """Saves citation to SQLite database."""
        
        citation_columns = ('key', 'citing_key', 'cited_key')
        row = (self.key, self.citing, self.cited)
        self.q.save_row_to_table("citations", row)
        
    def remove(self):
        """Removes citation from SQLite database."""
        
        self.q.remove_duplicate_rows("citations", self.key, all_but=0)

