.. role:: raw-html-m2r(raw)
   :format: html


Citation Graph
==============

What have people already done?
------------------------------


* 
  https://physics.stackexchange.com/questions/5569/is-there-a-nice-tool-to-plot-graphs-of-paper-citations

* 
  https://longair.net/blog/2009/10/21/thesis-visualization/

* 
  http://ongraphs.de/blog/2015/01/dynamic-citation-graph/ ***** Andre2015

* 
  http://bl.ocks.org/jose187/4733747 # a simple d3 network graph

* 
  https://academia.stackexchange.com/questions/83582/in-google-scholar-is-it-possible-to-view-the-list-of-papers-cited-by-a-specific

How would we go about this?
---------------------------


* 
  to visualise a graph, you need two lists: nodes and edges.

* 
  Andre2015's code should do the job. 
    His node lists include a simple counting id, the year of publication, the 'cyear' (?year first cited?), and a 'label' which gives the title.
    His edge ('link') lists include an edge id, the id of the citing work ('target'), the id of the cited work ('source'), and the year of citation (which is always the same as the year of publication of the citing work).

* 
  to generate these we need two, and ideally would have three tables (/dicts?):


  #. references in a book: {"Book1" : ["Book2","Book3","Book4"], ...}
  #. citations of a book: {"Book2": ["Book1",...], ...}
  #. and also the data for the book: [CitationKey, Author, Date, Title, Publisher, Abstract, ISBN, doi, ...]

* 
  Citations can be found on Google Scholar. We'll try to use Beautiful Soup and Requests or perhaps Selenium to scrape these...


  * Start here: https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=The+predictive+postcode%3A+the+geodemographic+classification+of+British+society&btnG=

* 
  References can be found in the text itself. If we can get copies of articles or bibliography chapters as PDFs, then we might be able to scrape these...


  * https://github.com/anderser/pydocsplit

* 
  Book data can be obtained from Zotero, if we have what Zotero calls an 'identifier': an ISBN, a doi, a PMID, or an arXiv id.


  * Can this be automated? 

    * https://forums.zotero.org/discussion/70995/perform-add-item-by-identifier-action-through-api
    * Most easily through Wikipedia's Zotero API: https://en.wikipedia.org/api/rest_v1/#/Citation/getCitation

* 
  Once you have all the data (saved in SQLite tables?), then you need to produce the json lists.


  * to produce the list of nodes, just run through table 3 which lists all the books.
  * to produce the list of edges, run through tables 1 and 2, generating all the edges.

MVP: Visualized graph of *Predictive Postcode*\ ,
---------------------------------------------------


* with full set of citations scraped from Google Scholar, 
* and full set of references gleaned from PDF of references chapter.
* Book data gained from Zotero and interpreted by pybtex (https://docs.pybtex.org/api/parsing.html)
* Data stored in :raw-html-m2r:`<del>SQLite database</del>` .bib files so that it's all human readable.

Or actually,


* instead of building a webscraper, let's for the moment just pull all the citations into Zotero using the Chrome toolbar plugin, 
    and use Zotero + BetterBibTex to generate a .bib citations file.
* and then let's just manually add some references to Zotero, and similarly generate a reference .bib file.
* then let's use pybtex to pull in those .bib files
* and then let's see if we can build an interface between a static front-end web-page using a JavaScript Fetch call 
    to pull in the relevant bibliographic data from a Flask API. https://pythonise.com/series/learning-flask/flask-and-fetch-api
* we might be able to automate the documentation for the API: https://flask-apispec.readthedocs.io/en/latest/

Okay, for tomorrow:


* add JS functionality:

  * when you call the API, you should *add* data to the front-end, not lose what's already there.
  * add some of the A-Z extra functionality: 

    * :raw-html-m2r:`<del>arrows</del>`
    * no overlap
    * :raw-html-m2r:`<del>(bigger circles)</del>`
    * highlighting
    * pinning down nodes
    * search

* scrape PDFs with Python (or even Ruby!)
* use pyzotero and scrape Google Scholar
* integrate literature.Text class into Flask API.

Another day, what have we done?


* we can easily make it so that you can drag a circle, and the data emerges in a nearby text box.
* we have managed to scrape pdfs, and we are beginning to learn regular expressions to identify at least the first line of the references.
* we thought that we could use this to scrape lots of useful information from google scholar and microsoft academic...
* but they both make it very difficult to automate this...
* though `some <https://mystudentvoices.com/scraping-google-scholar-to-write-your-phd-literature-chapter-2ea35f8f4fa1>`_ `people <http://thebiobucket.blogspot.com/2011/11/visually-examine-google-scholar-search.html>`_ seem to have done it...
* might be able to use selenium to make the mouse click on the link...

UML
---


.. image:: https://raw.githubusercontent.com/peterprescott/citation-graph/master/uml.gif
   :target: https://raw.githubusercontent.com/peterprescott/citation-graph/master/uml.gif
   :alt: Graphic UML
:raw-html-m2r:`<br>`
(Graphic generated by `Pynsource <https://pynsource.com/>`_\ , discovered through `StackOverflow <https://stackoverflow.com/questions/260165/whats-the-best-way-to-generate-a-uml-diagram-from-python-source-code>`_\ ).

Software (that will be) used:
-----------------------------


* Zotero
* Better Bibtex for Zotero (https://retorque.re/zotero-better-bibtex/citing/)
* Python
* Pybtex ( + documentation from https://www1.unipa.it/paolo.monella/pybtex/index.html)
* Pylint
* Pipenv
* Flask
* Sphinx (& ReadTheDocs) -- using Napoleon Extension & m2r
* Git (& GitHub)

Also...
-------


* `Open Citations <https://opencitations.wordpress.com/2018/02/25/citations-as-first-class-data-entities-the-opencitations-data-model/>`_ would be a great thing...
* http://opencitations.net/index
* http://opencitations.net/index/coci/api/v1
* https://figshare.com/articles/Open_Citation_Identifier_Definition/7127816
