# Citation Graph of Scholarly Literature

A second project ([here's the first](https://geodemographics.co.uk/projects/agent-based-modelling/)) done as part of [the Data CDT](https://datacdt.org/)'s [GEOG5995M/ENVS802 module](https://www.geog.leeds.ac.uk/courses/computing/study/core-python-phd/): **Programming For Social Scientists**.

Contents: [Task](#task). [Background Research](#research). [Software Design](#design). [Installation](#install). [Documentation](#docs).

<a id="task"></a>
# Task

Our [brief](https://www.geog.leeds.ac.uk/courses/computing/study/core-python-phd/assessment2/index.html) was as follows:

> *This assignment is a major project building up a model, application, or analysis from scratch. The project can be either something of your own invention, or one of the [suggested] projects... Broadly speaking, your project should:*
>
> *- Read in some data.*
>
> *- Process it in some way.*
>
> *- Display the results.*
>
> *- Write the results to a file.*

After a [brief attempt](https://github.com/peterprescott/sitelocation/blob/master/sitelocation.ipynb) at [one of the suggested projects](https://www.geog.leeds.ac.uk/courses/computing/study/core-python-phd/assessment2/best.html), I instead decided to do something relating more directly to my -- and potentially anyone's! -- PhD.

I decided to create some software to help visualize the webbed citation relationships of scholarly literature for an area of study, which for me is *The Geodemographics of British Streets*.

<a id="research"></a>
# Background Research

It turned out that what I was imagining is called a [citation network](https://en.wikipedia.org/wiki/Citation_network) or citation [graph](https://en.wikipedia.org/wiki/Graph_theory), which consists of *nodes* and *edges*.

Initial investigation confirmed I wasn't the only one who might find such a thing useful: [someone else (2011)](https://physics.stackexchange.com/questions/5569/is-there-a-nice-tool-to-plot-graphs-of-paper-citations)  was asking a similar question on StackExchange. I found a blog post from [Mark Longair (2009)](https://longair.net/blog/2009/10/21/thesis-visualization/) showing a graph of papers related to his thesis, scanned from PDFs he had collected. [Andre (2015)](http://ongraphs.de/blog/2015/01/dynamic-citation-graph/) had a very neat visualization comparing the citation networks of two related conferences, using "the force-directed layout engine included in d3.js", and linking to some examples: [Bostock (2017)](https://observablehq.com/@d3/force-directed-graph) and [Raper (2014)](http://www.coppelia.io/2014/07/an-a-to-z-of-extra-features-for-the-d3-force-layout/). 

All this suggested that what I was imagining would be possible, but would also require enough effort to make it a worthy project for this assignment.

It also suggested some possible ways of going about the task, both with regards to data collection (webscraping information from Google Scholar or Microsoft Academic, or scanning it from journal article PDFs) and data visualization (using [Graphviz](http://www.graphviz.org/) or [D3.js](https://d3js.org/)).

I also discovered [Zotero](https://en.wikipedia.org/wiki/Zotero), a "free and open source reference management system" which I hadn't come across before starting this course (I finished my undergraduate degree in 2010, and haven't been writing academic essays in the meantime). Zotero has a [web browser plug-in](https://www.zotero.org/download/connectors) which makes it simple to extract bibliographic information for literature referenced on the webpage you are browsing. I found that it uses [this Wikipedia API](https://en.wikipedia.org/api/rest_v1/#/Citation/getCitation) to generate citation data given an [ISBN](https://www.isbn-international.org/content/what-isbn) or [DOI](https://en.wikipedia.org/wiki/Digital_object_identifier).

Zotero allows bibliographic information to be exported as a *.bib* file, and I found that this can be parsed for Python by [Pybtex](https://pybtex.org/): "a BibTeX-compatible bibliography processor written in Python" that can be installed with `pip`. Zotero generates citation keys at time of export "using an algorithm that *usually* generates unique keys" -- [Better BibTex](https://retorque.re/zotero-better-bibtex/citing/) is a plug-in for Zotero that gives better control over citation keys. 

I also discovered [Open Citations](http://opencitations.net/), "a scholarly infrastructure organization dedicated to open scholarship"  and "engaged in advocacy for semantic publishing and open citations". They also have [an API](http://opencitations.net/index/coci/api/v1), for retrieving data about citations (ie. not the bibliographic data for an individual item, but the relational data about what each item cites and is cited by), but its dataset seems currently quite sparse, at least for my field of study.

<a id="running"></a>
# Software Design

## Basic Functionality

I decided to try and write a Python program that would be able to *read in data* from .bib files, from PDF files, and from the Zotero/Wikipedia API. It would *process this data* to get bibliographic information (minimally Author and Year of Publication, but ideally also Title, Item Type, Publisher, etc.) and citation relationships. It would use [D3.js Javascript](https://d3js.org/) running on [a static web page](https://www.netlify.com/pdf/oreilly-modern-web-development-on-the-jamstack.pdf) to *display the results* as an interactive visualization, obtaining the relevant data from the Python program by `fetch()`ing it from an API served by our Python program using [the Flask plug-in](https://palletsprojects.com/p/flask/). The program would also *write the results* to a SQLite database file.

## More Detailed Explanation (with UML Diagrams)

The Python program consists of five modules (files): `run.py`, `db_commands.py`, `literature.py`, `reader.py`, and `tests.py`.

![Module Relationships](https://raw.githubusercontent.com/peterprescott/citation-graph/master/packages.png)
Figure 1: Module Relationships

`run.py`

`db_commands.py`

`literature.py`

`reader.py`

`tests.py`

![Class Relationships](https://raw.githubusercontent.com/peterprescott/citation-graph/master/classes.png)
Figure 2: Class Relationships

These UML diagrams were automatically created using [pyreverse](https://www.logilab.org/blogentry/6883) with a single line of code:

```{console}
pyreverse *.py -o png
```
My only quibble would be that for some reason, pyreverse's automatically generated UML diagrams refers to my *modules* as *packages*, whereas in Python (as I understand thing at least) a ["module is a file containing Python definitions and statements"](https://docs.python.org/3/tutorial/modules.html), while a 'package' is ["is a directory which MUST contain a special file called __init__.py."](https://www.learnpython.org/en/Modules_and_Packages)

## Tests

Throughout the development of this program, I am trying to practise the principles of *Test-Driven Development* [(eg. Percival, 2017)](https://www.obeythetestinggoat.com/). This requires that before actually doing anything, we run a test that will check whether what we want to do is done. We run the test before writing the desired feature, so that it fails (obviously), then we write the feature, and then the test should run successfully.


## Virtual Environment & Package Installation Management

I have also used [Pipenv](https://pypi.org/project/pipenv/) to manage package installation within a contained virtual environment.

<a id="install"></a>
# Installation

You need to have Git and Python installed. If you don't, use your system's recommended package manager to download them from the command line. (For Windows, use [Chocolatey](https://chocolatey.org/install).)

Then clone the Github repository, and navigate into the project folder. You can then immediately run the model:

```console
python --version
git --version
git clone https://github.com/peterprescott/citation-graph
cd citation-graph
pipenv shell
python run.py
```
The program makes use of [Chris Mattmann's tika-python library](https://github.com/chrismattmann/tika-python), which allows Python to use [the Apache Tika toolkit](http://tika.apache.org/) for extracting data and metdata from PDFs. This does require that "Java 7+ installed on your system as tika-python starts up the Tika REST server in the background". Which is an added complication -- but it is quicker, more accurate, and simpler to use [Boylan-Toomey 2018](https://medium.com/@justinboylantoomey/fast-text-extraction-with-python-and-tika-41ac34b0fe61) than the other Python PDF libraries.

<a id="docs"></a>
# Documentation
[![Documentation Status](https://readthedocs.org/projects/citation-graph/badge/?version=latest)](https://citation-graph.readthedocs.io/en/latest/?badge=latest)

Documentation can be automatically generated by [Sphinx](https://www.sphinx-doc.org/en/master/usage/quickstart.html), which I learnt to use for [the previous project](https://github.com/peterprescott/agent-based-modelling). For this to work we have to make sure we write proper docstrings. We use [Google style](https://google.github.io/styleguide/pyguide.html#383-functions-and-methods), which means we require [the Napoleon extension](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) for Sphinx. We also use [m2r](https://github.com/miyakogi/m2r) to convert the README.md file to .rst so that it can be included.

Having generated it with Sphinx, we can also host the documentation freely at [ReadTheDocs.org](https://citation-graph.readthedocs.io/en/latest/). 
