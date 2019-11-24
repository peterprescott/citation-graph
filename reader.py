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
    
    def __init__(self, key):
        """Initializes PDF reader to extract and interpret references of text.
        
        Args:
            key (string): in BetterBibTex format [authForeIni][authEtAl][year].
            """
        
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
                ref = ref.replace('  ','')
                file.write(ref)
                file.write('\n')
                if print_refs: print(ref)
                tidied_refs.append(ref)
        self.references = tidied_refs
        return self.references

class Api():
    
    def __init__(self, doi=None):
        """Initializes API reader.
        
        Args:
            doi (string): Document Object Identifer; cf. https://www.doi.org/"""
        if doi: self.doi = doi
        
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
    print('hello reader')
    db_file = os.path.join(sys.path[0], 'citation_graph.db')
    new_keys = ['DTimms1975', 'RBurrowsGane2006', 'RKitchin2014']
    for new_key in new_keys: start = Bib(db_file, new_key)
    # ~ start=Bib(db_file, 'chapter')
    # ~ start.save()
