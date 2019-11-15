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
        # ~ return self.key
        return '\n'+ self.key + ': ' + self.title + ' (' + self.year +')'
    
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

        bib_data = parse_file(os.path.join('bib_files',f'{self.key}_citations.bib'))
        return bib_data
        
        self.type
        self.authors
        self.abstractmethod
        self.year
        self.publisher
        self.doi
        self.isbn
        self.length
        
# ~ class Author(object)

if __name__ == '__main__':
    ## run some simple tests.
    example_key = 'RWebberBurrows2018'
    example_text = Text(example_key)
    e = example_text
    print(type(e), e.key, e.references)
    # ~ for ref in e.references:
        # ~ print(type(ref))
