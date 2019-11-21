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

class Bib():
    """Uses pybtex to read .bib files (generated, at least in my case, by Zotero)."""
    
    def __init__(self, key):
        """Immediately read in citations and references, if files exist."""
        self.key = key
        if os.path.isfile(os.path.join('bib_files',f'{self.key}_citations.bib')):
            self.citations = parse_file(os.path.join('bib_files',f'{self.key}_citations.bib'))
        if os.path.isfile(os.path.join('bib_files',f'{self.key}_references.bib')):
            self.references = parse_file(os.path.join('bib_files',f'{self.key}_references.bib'))

    def save(self, citations=True, references=True):
        """Extract data and use appropriate literature class to save to db.
        
        Args:
            citations (Boolean): Extract citation data unless False.
            references (Boolean): Extract reference data unless False.
        """
        
        refs = self.references.entries
        # ~ print(ref_data.entries)
        db_file=os.path.join(sys.path[0], 'citation_graph.db')
        texts = []
        for entry in refs:
            # get key
            key = entry
            
            # get publication_year
            publication_year = str(refs[entry].fields['year']).replace('}','').replace('{','')
            
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
                    initial = creator.first_names[0][0]
                    creators_list.append({"surname" : surname, 
                                        "initial" : initial, 
                                        "role" : creator_type})
                    
            text_data = (key, publication_year, title, text_type, doi, creators_list)
            texts.append(text_data)
            
            if text_type == "book":
                publisher = refs[entry].fields['publisher']
                location = refs[entry].fields['address']
                number_of_pages = "unknown"
                isbn = refs[entry].fields['isbn']
                book_data = (publisher, location, number_of_pages, isbn)
                lit.Book(db_file, key, publication_year, title, text_type, 
                            location, number_of_pages, doi, isbn, creators_list)
                            
            if text_type == "incollection":
                print(refs[entry])
                title = refs[entry].fields['title']
                pages = refs[entry].fields['pages']
                chapter_data = (title, pages)
                
                publication_year = refs[entry].fields['year']
                book_title = refs[entry].fields['booktitle']
                publisher = refs[entry].fields['publisher']
                chapter_book_data = (book_key, publication_year, 
                        book_title, publisher, location, creators=book_creators)
            if text_type == "article":
                journal = refs[entry].fields['journal']
                volume = refs[entry].fields['volume']
                try:
                    edition = refs[entry].fields['number']
                except:
                    edition = None
                pages = refs[entry].fields['pages']
                article_data = (journal, volume, edition, pages)
                print(article_data)

    def json_graph(self):

        node_list = []
        edge_list = []
        
        ref_data = self.references
        
        for entry in ref_data.entries:
            node_list.append(
                            dict(id = entry, 
                                     title = str(ref_data.entries[entry].fields['title']).strip('{}'), 
                                     #author = str(ref_data.entries[entry].fields['author']).strip('{}'), 
                                     #year = str(ref_data.entries[entry].fields['year']).strip('{}'), 
                                     type = ref_data.entries[entry].type,
                                     group = 1
                                    )
                            )
            
            if entry != self.key:
                edge_list.append(dict(source = self.key, target = entry, value = 1))

        
        cite_data = self.citations
        
        for entry in cite_data.entries:
            if entry != self.key:
                node_list.append(
                                dict(id = entry, 
                                     title = str(cite_data.entries[entry].fields['title']).strip('{}'), 
                                     #author = str(cite_data.entries[entry].fields['author']).strip('{}'), 
                                     #year = str(cite_data.entries[entry].fields['year']).strip('{}'), 
                                     type = cite_data.entries[entry].type,
                                     group = 2
                                    )
                                )
                if entry != self.key:
                    edge_list.append(dict(source = entry, target = self.key, value = 1))
        
        
        return {"nodes": node_list, "links": edge_list}

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
    # ~ start = Bib('RWebberBurrows2018')
    start=Bib('chapter')
    start.save()
