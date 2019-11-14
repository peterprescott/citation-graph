# Citation Graph

## What have people already done?

- https://physics.stackexchange.com/questions/5569/is-there-a-nice-tool-to-plot-graphs-of-paper-citations

- https://longair.net/blog/2009/10/21/thesis-visualization/

- http://ongraphs.de/blog/2015/01/dynamic-citation-graph/ ***** Andre2015

- http://bl.ocks.org/jose187/4733747 # a simple d3 network graph

- https://academia.stackexchange.com/questions/83582/in-google-scholar-is-it-possible-to-view-the-list-of-papers-cited-by-a-specific

## How would we go about this?

- to visualise a graph, you need two lists: nodes and edges.

- Andre2015's code should do the job. 
    His node lists include a simple counting id, the year of publication, the 'cyear' (?year first cited?), and a 'label' which gives the title.
    His edge ('link') lists include an edge id, the id of the citing work ('target'), the id of the cited work ('source'), and the year of citation (which is always the same as the year of publication of the citing work).

- to generate these we need two, and ideally would have three tables (/dicts?):
    1. references in a book: {"Book1" : ["Book2","Book3","Book4"], ...}
    2. citations of a book: {"Book2": ["Book1",...], ...}
    3. and also the data for the book: [CitationKey, Author, Date, Title, Publisher, Abstract, ISBN, doi, ...]

- Citations can be found on Google Scholar. We'll try to use Beautiful Soup and Requests or perhaps Selenium to scrape these...
    - Start here: https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=The+predictive+postcode%3A+the+geodemographic+classification+of+British+society&btnG=

- References can be found in the text itself. If we can get copies of articles or bibliography chapters as PDFs, then we might be able to scrape these...
    - https://github.com/anderser/pydocsplit

- Book data can be obtained from Zotero, if we have what Zotero calls an 'identifier': an ISBN, a doi, a PMID, or an arXiv id.
    - Can this be automated? 
        - https://forums.zotero.org/discussion/70995/perform-add-item-by-identifier-action-through-api
        - Most easily through Wikipedia's Zotero API: https://en.wikipedia.org/api/rest_v1/#/Citation/getCitation
        
- Once you have all the data (saved in SQLite tables?), then you need to produce the json lists.
    - to produce the list of nodes, just run through table 3 which lists all the books.
    - to produce the list of edges, run through tables 1 and 2, generating all the edges.
    
    
