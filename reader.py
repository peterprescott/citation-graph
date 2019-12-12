"""
Contains class frameworks for parsing data from .bib files, .pdf files, and bibliographic/citation APIs respectively.

Can be run directly if there is new data you want to save to the database.

"""

import os.path
import sys
from pybtex.database import parse_file  # for parsing .bib files
from tika import unpack                 # for parsing .pdf files
# tika requires Java to be installed on your system: https://java.com/en/download/manual.jsp
# for some reason to make this work in Windows 7 I had to comment out line 546 in the tika.py file, to stop it throwing an error.
# in my case, this file was here: C:\Users\User\.virtualenvs\citation-graph-IlHssx7R\lib\site-packages\tika\tika.py
import codecs   # for reading utf-8 characters
import re       # for using regular expressions to descripe reference patterns
import requests # for fetching API JSON

import literature as lit
import db_commands as db

class Bib():
    """Uses pybtex to read .bib files (generated, at least in my case, by Zotero)."""
    
    def __init__(self, db_file, key):
        """Immediately read in citations and references, if files exist."""
        
        self.db_file = db_file
        self.key = key
        if os.path.isfile(os.path.join('bib_files',f'{self.key}_citations.bib')):
            self.citations = parse_file(os.path.join('bib_files',f'{self.key}_citations.bib'))
        else: self.citations = None
        if os.path.isfile(os.path.join('bib_files',f'{self.key}_references.bib')):
            self.references = parse_file(os.path.join('bib_files',f'{self.key}_references.bib'))
        else: self.references = None
        self._citations()
        self._text_data()

    def _citations(self):
        """Use literature classes to save Citations to db"""
        
        if self.citations:
            for entry in self.citations.entries:
                ref_key = str(entry)
                if ref_key != self.key:
                    lit.Citation(self.db_file, citing=ref_key, cited=self.key)
        
        if self.references:
            for entry in self.references.entries:
                ref_key = str(entry)
                if ref_key != self.key:
                    lit.Citation(self.db_file, citing=self.key, cited=ref_key)

    def _text_data(self):
        """Extract and save data for citation texts."""
        both = ['citations','references']
        for either in both:
            data = getattr(self, either)
            if data: 
                refs = data.entries
                texts = []
                for entry in refs:
                    ref_key = str(entry)
                    # get publication_year
                    try:
                        publication_year = str(refs[entry].fields['year']).replace('}','').replace('{','')
                    except KeyError:
                        publication_year = '?'
                    
                    # get title
                    title = str(refs[entry].fields['title']).replace('}','').replace('{','')
                    
                    # get text_type
                    text_type = refs[entry].type
                    
                    # try and get doi
                    try:
                        doi = refs.fields['doi']
                        print(doi)
                    except:
                        print('no doi')
                        doi = '?'

                    # get creators' data
                    creators_list = []
                    creators = refs[entry].persons
                    for creator_type in creators:
                        for creator in creators[creator_type]:
                            surname = creator.last_names[0]
                            try:
                                initial = creator.first_names[0][0]
                            except IndexError:
                                initial = ''
                            creators_list.append({"surname" : surname, 
                                                "initial" : initial, 
                                                "role" : creator_type})
                            
                    text_data = (ref_key, publication_year, title, text_type, doi, creators_list)
                    
                    if text_type == "book":
                        publisher, location, number_of_pages, isbn = self._book_details(refs, entry)
                        lit.Book(
                                self.db_file, ref_key, publication_year, title, publisher, 
                                location, number_of_pages, doi, isbn, creators=creators_list)
                                
                    elif text_type == "incollection":
                        pages, book_key, publisher, location = self._chapter_details(refs, entry)
                        lit.Chapter(
                                    self.db_file, ref_key, publication_year, title, publisher,
                                    location, pages, doi, creators=creators_list, book_key=book_key)
                                    
                    elif text_type == "article":
                        journal, volume, edition, pages = self._article_details(refs, entry)
                        lit.Article(self.db_file, ref_key, publication_year, title,
                                    journal, volume, edition, pages, doi,
                                    creators=creators_list)
                                    
                    else:
                        lit.Text(self.db_file, ref_key, publication_year, title, 
                                    text_type = "unknown", doi=doi, creators=creators_list)
                                
    def _book_details(self, refs, entry):
        """Get details specific to books."""

        try:
            publisher = refs[entry].fields['publisher']
        except KeyError:
            publisher = '?'
        try:
            location = refs[entry].fields['address']
        except KeyError:
            location = "?"
        number_of_pages = "unknown"
        try:
            isbn = refs[entry].fields['isbn']
        except KeyError:
            isbn = '?'
        return (publisher, location, number_of_pages, isbn)
        
    def _chapter_details(self, refs, entry):
        """Get details specific to chapter."""
        
        # get chapter details
        try:
            pages = refs[entry].fields['pages']
        except KeyError:
            pages = '?'
        
        # get details for book containing chapter
        try:
            book_title = refs[entry].fields['booktitle']
        except KeyError:
            book_title = None
        try:
            publisher = refs[entry].fields['publisher']
        except KeyError:
            publisher = '?'
        try:
            location = refs[entry].fields['address']
        except KeyError:
            location = "?"
        
        # try to match details for book containing chapter to known book
        if book_title:
            q = db.Query(self.db_file)
            match = q.search("texts", "title", book_title)
            if match: book_key = match[0][0]
            else: book_key = str(entry)+"<BOOK"
        else: book_key = str(entry)+"<BOOK"
        
        return (pages, book_key, publisher, location)
        
    def _article_details(self, refs, entry):
        """Get details specific to journal article."""

        try:
            journal = refs[entry].fields['journal']
        except KeyError:
            journal = '?'
        try:
            volume = refs[entry].fields['volume']
        except KeyError:
            volume = '?'
        try:
            edition = refs[entry].fields['number']
        except KeyError:
            edition = None
        try:
            pages = refs[entry].fields['pages']
        except KeyError:
            pages = '?'
        
        return (journal, volume, edition, pages)
        

class Pdf():
    
    def __init__(self, db_file, key):
        """Initializes PDF reader to extract and interpret references of text.
        
        Args:
            db_file (string): file location of database file.
            key (string): in BetterBibTex format [authForeIni][authEtAl][year].
            """
        
        self.db_file = db_file
        self.key = key
        self.pdf = f'{key}.pdf'
        self.txt = f"pdf2txt_{key}.txt"
        parsed = unpack.from_file(os.path.join('bib_files', self.pdf))
        with codecs.open(os.path.join('bib_files', self.txt), 'w', 'utf-8') as file:
            file.write(parsed['content'])
            
    def refs(self, print_refs=False):
        """ """
        
        extracted_text = ''
        with codecs.open(os.path.join('bib_files', self.txt), 'r', "utf-8") as file:
            for line in file:
                extracted_text += line
        self.references = re.findall(r"[A-Z].+[(](?:19|20)[\d][\d].*[)](?:[\n]|.)+?[.][\n]", extracted_text)
        
        self.ref_file = f"{self.key}_refs.txt"
        with codecs.open(os.path.join('bib_files', self.ref_file), 'w', "utf-8") as file:
            tidied_refs = []
            for ref in self.references:
                ref = ref.replace('\n',' ')
                ref = ref.replace('  ',' ')
                file.write(ref)
                file.write('\n')
                if print_refs: print(ref)
                tidied_refs.append(ref)
        self.references = tidied_refs
        return self.references
        
    def refs_parsed(self, check):
        """
        
        """
        
        self.check = check
        
        with codecs.open(os.path.join('bib_files', f"{self.key}_refs.txt"), 'r', "utf-8") as file:
            
            for line in file:
                check = self.check
                
                line = line.replace('  ',' ')
                
                # get creator(s) data
                creators_list = []
                creators = line.split('(')
                surnames = re.findall(r"[A-Z][A-Za-z ]+[,]", creators[0])
                initials = re.findall(r"[A-Z][.,\s]", creators[0])

                if len(surnames) == 1:
                    while len(initials) > 1:
                        initials.pop(1)

                if len(initials) != len(surnames): 
                    # TODO: Make sure initials are correct if multiple initials provided per author
                    pass
                    
                creator_count = len(surnames)
                
                # are these editors?
                editors = creators[1].split(')')[0]
                if editors[0] == 'e': creator_type = 'editor'
                else: creator_type = 'author'
                
                try:
                    for i in range(creator_count):
                        initial = initials[i]
                        surname = surnames[i]
                        creators_list.append({"surname" : surname.replace(' ','').replace('.','').replace(',',''), 
                                            "initial" : initial[0], 
                                            "role" : creator_type})
                except:
                    creators_list = []

                
                # get publication_year
                if creator_type == 'editor':
                    publication_year = creators[2].split(')')[0]
                else:
                    publication_year = creators[1].split(')')[0]
                 
                if len(publication_year) > 4:
                    if publication_year[4] in 'abcdefghijklm':
                        text_key_letter = publication_year[4]
                    publication_year = publication_year[0:4]
                
                try:
                    if creator_count == 1:
                        ref_key = creators_list[0]['initial']+creators_list[0]['surname']+publication_year
                    elif creator_count == 2:
                        ref_key = creators_list[0]['initial']+creators_list[0]['surname']+creators_list[1]['surname']+publication_year
                    elif creator_count > 2:
                        ref_key = creators_list[0]['initial']+creators_list[0]['surname']+"EtAl"+publication_year
                    else:
                        ref_key = "unknown"
                except:
                    ref_key = "unknown"
                
                # get item_type
                if re.search('[:]',line):
                    last_bit = line.split(':')[-1]
                    
                    # if a book, no page numbers at end of reference
                    if re.search(r"\d\d", last_bit)==None:
                        item_type = "book"
                        publisher = last_bit.replace('.','')
                        
                        middle_bit = re.findall(r"[)].+[:]",line)
                        try:
                            title = re.findall(r"[A-Z].+[.?!]", middle_bit[0])[0][0:-1]
                            location = middle_bit[0].split('.')[-1].replace(':','')
                            
                        except IndexError:
                            e = sys.exc_info()
                            print(f"\n\n\nERROR: {e}")
                        
                        # ~ print(f"\n\n{line}")
                        # ~ print(f"year = {publication_year}, title = {title}, publisher = {publisher}, location = {location}, creators = {creators_list}")
                        # ~ input('Is that right?')
                        
                        if ref_key != "unknown":
                            if check != "y":
                                print(f"\n\n{line}")
                                print(f"ref_key:{ref_key}\npublication_year:{publication_year}\ntitle:{title}\npublisher:{publisher}\nlocation:{location}\ncreators:{creators_list}")
                                check = input("Enter 'y' to accept, or anything else to move on to the next entry.\n>>> ")
                            if check=="y":
                                lit.Book(
                                    self.db_file, ref_key, publication_year, title, publisher, 
                                    location, creators=creators_list)
                        
                    # if a chapter, letters as well as page numbers
                    elif re.findall(r"[A-Za-z]+", last_bit):
                        test = re.findall(r"[A-Za-z]+", last_bit)
                        
                        try:
                            title = re.findall(r"‘.+’", line)
                            title = title[0][1:-1]

                        except IndexError:
                            title = "unknown"
                        
                        middle_bit = re.findall(r"[)].+[:]",line)
                        
                        try:
                            middle_bit[0] = middle_bit[0].replace('?','.')
                            location = middle_bit[0].split('.')[-1].replace(':','')
                        except:
                            location = "unknown"
                        
                        try:
                            book_info = re.findall(r"’[,\s] in .+[.?!]", middle_bit[0])[0]
                            book_title = re.findall(r"[)].+", book_info)[0][2:-1]
                            
                        except IndexError:
                            book_title = "unknown"
                            e = sys.exc_info()
                            print(f"\n\n\nERROR: {e}")

                        try:
                            book_info = re.findall(r"’[,\s] in .+[.?!]", middle_bit[0])[0]
                            book_authors = re.findall(r".+[(]", book_info)[0]
                            surnames = re.findall(r"[A-Z][A-Za-z ]+", book_authors)
                            initials = re.findall(r"[A-Z][.,\s]", book_authors)

                            if len(surnames) == 1:
                                while len(initials) > 1:
                                    initials.pop(1)

                            if len(initials) != len(surnames): 
                                # TODO: Make sure initials are correct if multiple initials provided per author
                                pass
                            
                            book_creators  = []
                            
                            for i in range(len(surnames)):
                                initial = initials[i][0]
                                surname = surnames[i].replace(' ','').replace('.','').replace(',','')
                                book_creators.append({"surname" : surname, 
                                                    "initial" : initial, 
                                                    "role" : "editor"})
                                                    
                            if len(surnames) == 1:
                                book_key = book_creators[0]['initial']+book_creators[0]['surname']+publication_year
                            elif len(surnames) == 2:
                                book_key = book_creators[0]['initial']+book_creators[0]['surname']+book_creators[1]['surname']+publication_year
                            elif len(surnames) > 2:
                                book_key = book_creators[0]['initial']+book_creators[0]['surname']+"EtAl"+publication_year


                        except:
                            e = sys.exc_info()
                            # ~ print(f"\n\n\nERROR: {e}")
                            
                        try:
                            book_key
                        except:
                            book_key = "unknown"
                            book_creators = []
                            
                        item_type = "chapter"

                        try:
                            [publisher, pages] = last_bit.split(',')[0], last_bit.split(',')[1]

                        except IndexError:
                            # ~ print(f"IndexError ~ {last_bit}")
                            text_type = "website"
                            web_address = location + last_bit
                            web_address = web_address.replace('Available at ','')
                            # ~ print(f"URL: {web_address}")
                            
                        if item_type == "chapter":
                            if ref_key != "unknown":
                                if check != "y":
                                    print(f"\n\n{line}")
                                    print(f"""ref_key:{ref_key}\npublication_year:{publication_year}\ntitle:{title}\n
                                            publisher:{publisher}\nlocation:{location}\ncreators:{creators_list}\n
                                            book_key:{book_key}\nbook_title:{book_title}\nbook_creators:{book_creators}""")
                                    check = input("Enter 'y' to accept, or anything else to move on to the next entry.\n>>> ")
                                    if ref_key != "unknown":
                                        if check=="y":
                                            lit.Chapter(
                                                        self.db_file, ref_key, publication_year, title,
                                                        publisher, location, pages, creators=creators_list,
                                                        book_key=book_key, book_title=book_title, book=None,
                                                        book_creators=book_creators)
                    
                    # otherwise just (page) numbers ==> article
                    else:
                        item_type = "article"
                        pages = publisher # it's not actually a publisher, it's a list of pages.
                        pages = re.findall(r"[\d].*[\d]", last_bit)[0]
                        
                        try:
                            title = re.findall(r"‘.+’", line)
                            title = title[0][1:-1]
                        except IndexError:
                            title = "unknown"
                            
                        journal_info = line.split('’')[-1]
                        
                        try:
                            journal = re.findall(r"[\s].+[,]", journal_info)[0]
                        except:
                            journal = "unknown"
                            
                        try:
                            volume = re.findall(r"[\d]+[\s]*[(]", journal_info)[0][0:-1]
                            edition = re.findall(r"[(][\d]+[)]", journal_info)[0][1:-1]
                        except IndexError:
                            e = sys.exc_info()
                            print(f"\n\n\nERROR: {e}")

                        if len(journal) == 0:
                            print(f"\n\n{line}")
                        else:
                            journal = journal[1:-1]

                        if ref_key != "unknown":
                            if check != "y":
                                print(f"\n\n{line}")
                                print(f"ref_key:{ref_key}\npublication_year:{publication_year}\ntitle:{title}\njournal:{journal}\nvolume:{volume}\nedition:{edition}\npages:{pages}\ncreators:{creators_list}")
                                check = input("Enter 'y' to accept, or anything else to move on to the next entry.\n>>> ")
                            if check=="y":
                                lit.Article(
                                    self.db_file, ref_key, publication_year, title,
                                    journal, volume, edition, pages,
                                    creators=creators_list)
                                    
                        
                else:
                    item_type = "unknown"
                    
                    if ref_key != "unknown":
                    
                        if check != "y":
                            print(f"\n\n{line}")
                            print(f"ref_key:{ref_key}, publication_year:{publication_year}, creators:{creators_list}")
                            check = input("Enter 'y' to accept, or anything else to move on to the next entry.\n>>> ")
                        if check=="y":
                            lit.Text(self.db_file, ref_key, publication_year, text_type = "unknown", creators=creators_list)

                if ref_key != "unknown":
                    if check=="y":
                        lit.Citation(self.db_file, self.key, ref_key)

                
                



class Api():
    
    def __init__(self, doi):
        """
        Initializes API reader.
        
        Args:
            doi (string): Document Object Identifer; cf. https://www.doi.org/
        """
        self.doi = doi
        
        
    def data(self, choose="all"):
        """
        Fetch DOI, citations and reference data from APIs.
        """
        doi_api = "https://en.wikipedia.org/api/rest_v1/data/citation/zotero"
        citations_api = "http://opencitations.net/index/coci/api/v1/citations"
        references_api = "http://opencitations.net/index/coci/api/v1/references"
        
        if choose == "doi" or choose == 0:
            doi_without_slash = self.doi.replace('/','%2f')
            self.doi_data = requests.get(f'{doi_api}/{doi_without_slash}')
            # this API accepts ISBNs as well as DOIs, see documentation:
            # https://en.wikipedia.org/api/rest_v1/#/Citation/getCitation
            return self.doi_data
        elif choose == "citations" or choose == 1:
            self.citation_data = requests.get(f'{citations_api}/{self.doi}')
            # see documentation: http://opencitations.net/index/coci/api/v1/
            return self.citation_data
        elif choose == "references" or choose == 2:
            self.reference_data = requests.get(f'{references_api}/{self.doi}')
            # see documentation: http://opencitations.net/index/coci/api/v1/
            return self.reference_data
        else:
            doi_without_slash = self.doi.replace('/','%2f')
            self.doi_data = requests.get(f'{doi_api}/{doi_without_slash}')
            self.citation_data = requests.get(f'{citations_api}/{self.doi}')
            self.reference_data = requests.get(f'{references_api}/{self.doi}')
            return [self.doi_data, self.citation_data, self.reference_data]
            

if __name__ == '__main__':
    db_file = os.path.join(sys.path[0], 'citation_graph.db')
    new_keys = ['DTimms1975']
    for new_key in new_keys: start = Bib(db_file, new_key)
    # ~ start=Bib(db_file, 'chapter')
    # ~ start.save()

    # ~ get = Pdf(db_file, 'EWily2015')
    # ~ get.refs(True)
    # ~ get.refs_parsed("check")
