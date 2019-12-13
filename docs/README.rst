.. role:: raw-html-m2r(raw)
   :format: html


Citation Graph of Scholarly Literature
======================================

A second project done as part of `the Data CDT <https://datacdt.org/>`_\ 's `GEOG5995M/ENVS802 module <https://www.geog.leeds.ac.uk/courses/computing/study/core-python-phd/>`_\ : **Programming For Social Scientists**.

It is 'licensed' under the `The Unlicense <https://unlicense.org/>`_\ , and available on `my Github <https://github.com/peterprescott/citation-graph>`_.

README Contents:  `Installation and Quickstart <#install>`_. `Task <#task>`_. `Background Research <#research>`_. `Software Design <#design>`_. `Documentation <#docs>`_.

:raw-html-m2r:`<a id="install"></a>`

Installation and Quickstart
===========================

To run this on your machine you need to have Git and Python installed. If you don't, use your system's recommended package manager to download them from the command line. (For Windows, use `Chocolatey <https://chocolatey.org/install>`_.)

Then clone the Github repository, and navigate into the project folder. You can then immediately run the program:

.. code-block:: console

   python --version
   git --version
   git clone https://github.com/peterprescott/citation-graph
   cd citation-graph
   pip install pipenv
   pipenv shell
   pipenv install
   python run.py

The program will be initially running on data that I've already entered, saved in the SQLite database ``citation-graph.db``. (Note that the visualized nodes do sometimes get stuck in the top left of their SVG field -- if that happens just click-and-drag them down with your mouse cursor). 

To prove the functionality of the program, let's delete the database file, and then recreate it.

.. code-block:: console

   rm citation-graph.db

You can still keep the web-page interface open, but if you try clicking *Load More Data*\ , the Python code will report ``sqlite3.OperationalError: no such table: texts``. But we can quickly recreate the database (which is generated from .bib files in the ``bib_files\`` folder -- more on that later!)

.. code-block::

   pipenv shell
   python db_commands.py
   python reader.py load
   python run.py

Now you will be able to *Load More Data*. And indeed if you want you are able to load your own data. 

But let's slow down and start at the beginning...

:raw-html-m2r:`<a id="task"></a>`

Task
====

Our `brief <https://www.geog.leeds.ac.uk/courses/computing/study/core-python-phd/assessment2/index.html>`_ for this assignment was as follows:

..

   *This assignment is a major project building up a model, application, or analysis from scratch. The project can be either something of your own invention, or one of the [suggested] projects... Broadly speaking, your project should:*

   *- Read in some data.*

   *- Process it in some way.*

   *- Display the results.*

   *- Write the results to a file.*


After a `brief attempt <https://github.com/peterprescott/sitelocation/blob/master/sitelocation.ipynb>`_ at `one of the suggested projects <https://www.geog.leeds.ac.uk/courses/computing/study/core-python-phd/assessment2/best.html>`_\ , I instead decided to do something relating more directly to my -- and potentially anyone's! -- PhD. I decided to create some software to help visualize the webbed citation relationships of scholarly literature for an area of study. Every PhD begins with a *Literature Review*\ , surveying the state of knowledge in some particular area of scholarly knowledge, and surely a PhD in Data Analytics should at least try to make use of the tools of data analysis in that essential initial task!

:raw-html-m2r:`<a id="research"></a>`

Background Research
===================

It turned out that what I was imagining is called a `citation network <https://en.wikipedia.org/wiki/Citation_network>`_ or citation `graph <https://en.wikipedia.org/wiki/Graph_theory>`_\ , which consists of *nodes* and *edges*.

Initial investigation confirmed I wasn't the only one who might find such a thing useful: `someone else (2011) <https://physics.stackexchange.com/questions/5569/is-there-a-nice-tool-to-plot-graphs-of-paper-citations>`_  was asking a similar question on StackExchange. I found a blog post from `Mark Longair (2009) <https://longair.net/blog/2009/10/21/thesis-visualization/>`_ showing a graph of papers related to his thesis, scanned from PDFs he had collected. `Andre (2015) <http://ongraphs.de/blog/2015/01/dynamic-citation-graph/>`_ had a very neat visualization comparing the citation networks of two related conferences, using "the force-directed layout engine included in d3.js", and linking to some examples: `Bostock (2017) <https://observablehq.com/@d3/force-directed-graph>`_ and `Raper (2014) <http://www.coppelia.io/2014/07/an-a-to-z-of-extra-features-for-the-d3-force-layout/>`_. 

All this suggested that what I was imagining would be possible, but would also require enough effort to make it a worthy project for this assignment.

It also suggested some possible ways of going about the task, both with regards to data collection (webscraping information from Google Scholar or Microsoft Academic, or scanning it from journal article PDFs) and data visualization (using `Graphviz <http://www.graphviz.org/>`_ or `D3.js <https://d3js.org/>`_\ ).

I also discovered `Zotero <https://en.wikipedia.org/wiki/Zotero>`_\ , a "free and open source reference management system" which I hadn't come across before starting this course (I finished my undergraduate degree in 2010, and haven't been writing academic essays in the meantime). Zotero has a `web browser plug-in <https://www.zotero.org/download/connectors>`_ which makes it simple to extract bibliographic information for literature referenced on the webpage you are browsing. I found that it uses `this Wikipedia API <https://en.wikipedia.org/api/rest_v1/#/Citation/getCitation>`_ to generate citation data given an `ISBN <https://www.isbn-international.org/content/what-isbn>`_ or `DOI <https://en.wikipedia.org/wiki/Digital_object_identifier>`_.

Zotero allows bibliographic information to be exported as a *.bib* file, and I found that this can be parsed for Python by `Pybtex <https://pybtex.org/>`_\ : "a BibTeX-compatible bibliography processor written in Python" that can be installed with ``pip``. Zotero generates citation keys at time of export "using an algorithm that *usually* generates unique keys" -- `Better BibTex <https://retorque.re/zotero-better-bibtex/citing/>`_ is a plug-in for Zotero that gives better control over citation keys. 

I also discovered `Open Citations <http://opencitations.net/>`_\ , "a scholarly infrastructure organization dedicated to open scholarship"  and "engaged in advocacy for semantic publishing and open citations". They also have `an API <http://opencitations.net/index/coci/api/v1>`_\ , for retrieving data about citations (ie. not the bibliographic data for an individual item, but the relational data about what each item cites and is cited by), but its dataset seems currently quite sparse, at least for my field of study.

:raw-html-m2r:`<a id="running"></a>`

Software Design
===============

Basic Functionality
-------------------

I decided to try and write a Python program that would be able to *read in data* from .bib files, from PDF files, and from the Zotero/Wikipedia API. It would *process this data* to get bibliographic information (minimally Author and Year of Publication, but ideally also Title, Item Type, Publisher, etc.) and citation relationships. It would use `D3.js Javascript <https://d3js.org/>`_ running on `a static web page <https://www.netlify.com/pdf/oreilly-modern-web-development-on-the-jamstack.pdf>`_ to *display the results* as an interactive visualization, obtaining the relevant data from the Python program by ``fetch()``\ ing it from an API served by our Python program using `the Flask plug-in <https://palletsprojects.com/p/flask/>`_. The program would also *write the results* to a `SQLite <https://docs.python.org/2/library/sqlite3.html>`_ database file.

More Detailed Explanation (with UML Diagrams)
---------------------------------------------

The essential software consists of five modules (\ ``run.py``\ , ``db_commands.py``\ , ``literature.py``\ , ``reader.py``\ , and ``tests.py``\ ), a static browser interface (\ ``static_gui\index.html``\ , ``static_gui\graph.css``\ , and ``static_gui\script.js``\ ), a SQLite database (\ ``citation_graph.db``\ ). If this database is deleted, any data it contains will be lost, but a new (initially empty) file with the same name will be generated when the program is next run.

There are also subfolders: ``test_output\`` contains a ``logs.txt`` file with automated reports from the tests that were run as this program was written; ``docs\`` contains all the necessary files for autogenerating Sphinx documentation (to rebuild the docs on Windows, one can simply run ``rebuild_docs.bat``\ ); ``bib_files`` contains *.bib* and *.pdf* files from which the program reads bibliographic and citational information; and of course ``.git\`` makes sure that we can keep track of all of our version changes.

There are also a few other odd files:
``Pipfile`` and ``Pipfile.lock`` are used by ``pipenv`` to load and keep track of the necessary virtual environment, and all its installed packages.
``uml.bat`` (Windows) and ``uml.bash`` (Linux) call ``pyreverse`` to autogenerate UML diagrams, which are saved as ``packages.png`` and ``classes.png``.
``chromedriver.exe`` is necessary for the ``tests.py`` module to use ``selenium`` to control Chrome and test that the Flask API is working correctly.
``.readthedocs.yml`` provides `ReadtheDocs.org <https://readthedocs.org/>`_ with the necessary information to generate and host documentation.
``.gitignore`` tells git to ignore specified autogenerated files and folders which don't need keeping.

``static_gui\``
^^^^^^^^^^^^^^^^^^^

``index.html``\ , ``graph.css``\ , ``script.js``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A simple static site interface is used for graphic visualization.

The static site interface (separated of course into its HTML, CSS, and JS components) is influenced by `modern JAMstack principles <https://www.netlify.com/pdf/oreilly-modern-web-development-on-the-jamstack.pdf>`_ which suggest enabling dynamic interactivity on fundamentally static web-pages by using front-end Javascript in combination with cloud-hosted APIs, which increases speed, security and simplicity compared to the traditional 'dynamic web-page' served live (most commonly with the `LAMPstack <https://en.wikipedia.org/wiki/LAMP_(software_bundle>`_\ ).

As an example, I have set up a cloud-hosted copy of this program at `citations.pythonanywhere.com <https://citations.pythonanywhere.com>`_\ , and a corresponding static interface on `my own static site <https://geodemographics.co.uk/citations>`_.

But a static site can also engage with an API served locally, as is the primary intention here.

``run.py``
^^^^^^^^^^^^^^

This is the main file intended to be run. It first opens static_gui/index.html in your default webbrowser, and then serves the Flask API which is called from that static interface. When called it responds with the required graph data by returning a JSON object with the necessary nodes and edges.

Read the full documentation `here <https://citation-graph.readthedocs.io/en/latest/run.html>`_\ , or examine the source code directly `here <https://github.com/peterprescott/citation-graph/blob/master/run.py>`_.


.. image:: https://raw.githubusercontent.com/peterprescott/citation-graph/master/packages.png
   :target: https://raw.githubusercontent.com/peterprescott/citation-graph/master/packages.png
   :alt: Module Relationships

*Figure 1: Module Relationships*

``reader.py``
^^^^^^^^^^^^^^^^^

Contains class frameworks for parsing data from .bib files (Bib), .pdf files (Pdf), and bibliographic/citation APIs (Api) respectively.

Can be run directly from the command-line if there is new data you want to save to the database, like so:

.. code-block::

   python reader.py citationkey

where *citationkey* is the citation key of a .pdf file (ie. citationkey.pdf) 
including references (ie. journal article or bibliography chapter) or 
.bib file (ie. citationkey_citations.bib or citationkey_references.bib) 
in the bib_files folder.

Running ``python reader.py load`` should load the six bib_files that I have already put in the folder as a demonstration.

NB: .bib files can be generated by Zotero, ideally using the BetterBibTex format [authForeIni][authEtAl][year]. Create a unique Subcollection with the item referred to by the citation key, together with a selection of works it references, or which cite it, and export it to a .bib file named accordingly.

Parsing .bib files makes use of Pybtex.

Parsing .pdf files makes use of `Chris Mattmann's tika-python library <https://github.com/chrismattmann/tika-python>`_\ , which allows Python to use `the Apache Tika toolkit <http://tika.apache.org/>`_ for extracting data and metdata from PDFs. This does require that "Java 7+ installed on your system as tika-python starts up the Tika REST server in the background". Which is an added complication -- but it is quicker, more accurate, and simpler to use (\ `Boylan-Toomey, 2018 <https://medium.com/@justinboylantoomey/fast-text-extraction-with-python-and-tika-41ac34b0fe61>`_\ ) than the other Python PDF libraries.

Once Tika has extracted the text from the PDF, it is then written to a text-file. This is then parsed using `\ *regular expressions* <https://docs.python.org/3/library/re.html>`_ for making sense of that data. Unfortunately the standardization of 'Harvard style' is still vague enough that there is a lot of variation, which makes it difficult to generalize a formula for automatically extracting the references from a journal article or book. Currently the algorithm is calibrated to read the references from our initial example starting point: Webber, R., Burrows, R., (2018), *The Predictive Postcode*\ ; the reference chapter of which is saved as ``RWebberBurrows2018.pdf`` in the ``bib_files\`` folder.

Read the full documentation `here <https://citation-graph.readthedocs.io/en/latest/reader.html>`_\ , or examine the source code directly `here <https://github.com/peterprescott/citation-graph/blob/master/reader.py>`_.

``literature.py``
^^^^^^^^^^^^^^^^^^^^^

Class frameworks for: Text, Book, Chapter, Article, Creator, Citation.

Book, Chapter, and Article are all daughter classes of Text.

All literature classes use ``Query()`` from ``db_commands.py`` to save data.

Read the full documentation `here <https://citation-graph.readthedocs.io/en/latest/literature.html>`_\ , or examine the source code directly `here <https://github.com/peterprescott/citation-graph/blob/master/literature.py>`_.

``db_commands.py``
^^^^^^^^^^^^^^^^^^^^^^

Includes a variety of commands to make querying the SQLite database simple, encapsulated in a class framework called Query.

When run directly it builds the necessary tables to run the Citation Graph program,
for if and when the database is deleted.

Read the full documentation `here <https://citation-graph.readthedocs.io/en/latest/db_commands.html>`_\ , or examine the source code directly `here <https://github.com/peterprescott/citation-graph/blob/master/db_commands.py>`_.

``tests.py``
^^^^^^^^^^^^^^^^

Runs tests (encapsulated in a Test class) and documents results in ``test_output/logs.txt``.

Read the full documentation `here <https://citation-graph.readthedocs.io/en/latest/tests.html>`_\ , or examine the source code directly `here <https://github.com/peterprescott/citation-graph/blob/master/tests.py>`_.


.. image:: https://raw.githubusercontent.com/peterprescott/citation-graph/master/classes.png
   :target: https://raw.githubusercontent.com/peterprescott/citation-graph/master/classes.png
   :alt: Class Relationships

*Figure 2: Class Relationships*

These UML diagrams were automatically created using `pyreverse <https://www.logilab.org/blogentry/6883>`_.

Tests
-----

Throughout the development of this program, I am trying to practise the principles of *Test-Driven Development* `(eg. Percival, 2017) <https://www.obeythetestinggoat.com/>`_. This requires that before actually doing anything, we run a test that will check whether what we want to do is done. We run the test before writing the desired feature, so that it fails (obviously), then we write the feature, and then the test should run successfully.

Virtual Environment & Package Installation Management
-----------------------------------------------------

I have also used `Pipenv <https://pypi.org/project/pipenv/>`_ to manage package installation within a contained virtual environment.

:raw-html-m2r:`<a id="docs"></a>`

Documentation
=============


.. image:: https://readthedocs.org/projects/citation-graph/badge/?version=latest
   :target: https://citation-graph.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


Documentation can be automatically generated by `Sphinx <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_\ , which I learnt to use for `the previous project <https://github.com/peterprescott/agent-based-modelling>`_. For this to work we have to make sure we write proper docstrings. We use `Google style <https://google.github.io/styleguide/pyguide.html#383-functions-and-methods>`_\ , which means we require `the Napoleon extension <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_ for Sphinx. We also use `m2r <https://github.com/miyakogi/m2r>`_ to convert the README.md file to .rst so that it can be included.

Having generated it with Sphinx, we can also host the documentation freely at `ReadTheDocs.org <https://citation-graph.readthedocs.io/en/latest/>`_. 
