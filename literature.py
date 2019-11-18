import os.path
from pybtex.database import parse_file  # for parsing .bib files
import inspect

# ~ def get_citations(key):

    # ~ bib_data = parse_file(os.path.join('bib_files',f'{key}_citations.bib'))
    # ~ return bib_data

# ~ def get_references(key):

    # ~ bib_data = parse_file(os.path.join('bib_files',f'{key}_references.bib'))
    # ~ return bib_data


class Text(object):
    
    def __init__(self, key, pybtex_data = None):
        """
        Initialize Text.
        
        Args:
            key (string): unique Better BibTeX citation key 
                in form [authForeIni][authEtAl][year].
            pybtex_data (pybtex.database.Entry): relevant data from .bib file.
        """
        
        self.key = key
        if os.path.exists(os.path.join('bib_files',f'{key}_references.bib')):
            self.ref_data = True
        else: self.ref_data = False
        if os.path.exists(os.path.join('bib_files',f'{key}_citations.bib')):
            self.cite_data = True
        else: self.cite_data = False
        self.references = []
        self.citations = []
        self.detailed = False
        self.pybtex_data = pybtex_data


        if self.ref_data:
            self.get_references()
        if self.cite_data:
            self.get_citations()
        if self.pybtex_data:
            self.get_detail(pybtex_data)
    
    def __repr__(self):
        """ """
        # ~ return self.key
        return '\n'+ self.key + ': ' + self.title
    
    def get_detail(self, pybtex_data=None):
        if pybtex_data: 
            self.type = self.pybtex_data.type
            for field in self.pybtex_data.fields:
                setattr(self, field, self.pybtex_data.fields[field].replace('}','').replace('{',''))
            self.detailed = True
        else:
            self.get_references()
        
    def get_references(self):
        
        if self.references != []:
            return self.references
        elif self.ref_data:
            bib_data = parse_file(os.path.join('bib_files',f'{self.key}_references.bib'))
            bib_data.entries[self.key]
            for entry in bib_data.entries:
                if entry != self.key:
                    self.references.append(Text(entry, bib_data.entries[entry]))
            return self.references
        else:
            message = 'There are no references!'
            print(message)
            return []
        
    def get_citations(self):

        if self.citations != []:
            return self.citations
        elif self.cite_data:
            bib_data = parse_file(os.path.join('bib_files',f'{self.key}_citations.bib'))
            bib_data.entries[self.key]
            for entry in bib_data.entries:
                if entry != self.key:
                    self.references.append(Text(entry, bib_data.entries[entry]))
            return self.citations
        else:
            message = 'There are no citations!'
            print(message)
            return []





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
# [{"itemType":"book","creators":[{"creatorType":"author","firstName":"","lastName":"Timms, Duncan."}],"date":"1971","publisher":"University Press","title":"The urban mosaic : towards a theory of residential differentiation","ISBN":"0521079640, 9780521079648","place":"Cambridge [England]","numPages":"viii, 277 pages","oclc":"132648","url":"https://www.worldcat.org/oclc/132648","accessDate":"2019-11-18"}]
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

