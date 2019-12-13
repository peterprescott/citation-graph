"""Runs tests (encapsulated in a Test class) and documents results in `test_output/logs.txt`"""

from datetime import datetime   # for recording data and time of tests
from selenium import webdriver  # for testing web app
import sqlite3                  # for testing database
import os                       # for navigating between folders
import sys

import db_commands as db
import reader
import literature as lit


class Test():
    
    def __init__(self):
        self.tests = 0
        self.success = 0
        with open(os.path.join(sys.path[0], 'test_output', 'logs.txt'), 'a') as log:
            now = datetime.now()
            log.write("\n" + now.strftime("%d/%m/%Y %H:%M:%S"))
            log.write(self.logic())
            # ~ log.write(self.flask_app("localhost:5000/test", "Running!"))
            log.write(self.db_commands())
            log.write(self.bib_reader())
            log.write(self.pdf_reader())
            # ~ log.write(self.api_interactions())
            log.write(self.lit_classes())
            # ~ log.write(self.jamstack_gui())
            # ~ log.write(self.web_scraper())
            summary = f"\nRan {self.tests} tests: {self.success}/{self.tests} were successful."
            print(summary)
            log.write(summary)
            log.write("\n")
        
    def logic(self):
        """
        Shows that the basic logic of my Test framework works.
        """
        
        self.tests += 1
        
        try:
            assert True == True
            self.success += 1
            result = "\nTest Successful: Logic working as expected."
        except:
            e = sys.exc_info()
            print(f"\n\n\nERROR: {e}")
            result = "\nTest Failed: Logic not working as expected."
        
        print(result)
        return result


    def flask_app(self, page_location, confirmation):
        """
        Tests that Flask App is running as expected.

        Uses Selenium Webdriver to check Flask App is running as expected.

        Args:
            URL (string): the address where the Flask App is running.
            page_title (string): the title of the webpage,
                as it should be defined by <title> tags.
        """

        self.tests += 1

        driver = webdriver.Chrome(os.path.join(sys.path[0], 'chromedriver.exe'))
        driver.get(page_location)
        print(driver)
        if driver.title == confirmation:
            self.success += 1
            result = "\nTest Successful: Flask App running as expected."
        else:
            e = sys.exc_info()
            print(f"\n\n\nERROR: {e}")
            result = """\nTest Failed: Flask App not running as expected. 
                    (It may not be broken -- you need to run it explicitly.)"""
        
        print(result)
        return result

    def db_commands(self):
        """
        Tests that database commands from ../db_commands.py are working as expected.
        
        Args:
            file (string): file location for db_commands.py
        """ 
        
        self.tests += 1
        
        details = ""

        try:
            q = db.Query(os.path.join(sys.path[0], 'citation_graph.db'))
            assert q.test() == "connected"
            details += '\n>>>Connection working'
            q.create_table('test_table', ('key', 'other_column'))
            details += '\n>>>create_table() working'
            q.save_row_to_table('test_table', ('test_key', 'testing_testing'))
            details += '\n>>>save_row_to_table() working'
            assert q.search('test_table', 'key', 'test_key')[0] == ('test_key', 'testing_testing')
            details += '\n>>>search() working'
            q.remove_row('test_table', 1)
            details += '\n>>>remove_row() working'
            assert len(q.search('test_table', 'key', 'test_key')) == 0
            q.save_row_to_table('test_table', ('test_key', 'testing_testing'), allow_duplicate=True)
            q.save_row_to_table('test_table', ('test_key', 'testing_testing'), allow_duplicate=True)
            assert len(q.search('test_table', 'key', 'test_key')) == 2
            details += '\n>>>testing remove_duplicate_rows()'
            q.remove_duplicate_rows('test_table', 'test_key')
            assert len(q.search('test_table', 'key', 'test_key')) == 1
            details += '\n>>>remove_duplicate_rows() working'
            q.drop_table('test_table')
            details += '\n>>>drop_table() working'
            self.success += 1
            result = "\nTest Successful: Database Commands working as expected."
        except:
            e = sys.exc_info()
            print(f"\n\n\nERROR: {e}")
            result = "\nTest Failed: Database Commands not working as expected."
            result += details
        print(result)
        return result
        
    def bib_reader(self):
        """
        Tests that reader.py is able to read in .bib files by running a check
        on the _references.bib and _citations.bib files for @RWebberBurrows2018.
        """
        
        self.tests += 1
        
        try:
            db_file = os.path.join(sys.path[0], 'citation_graph.db')
            start = reader.Bib(db_file, 'RWebberBurrows2018')
            self.success += 1
            result = "\nTest Successful: .bib Reader working as expected."
        except:
            e = sys.exc_info()
            print(f"\n\n\nERROR: {e}")
            result = """\nTest Failed: .bib Reader not working as expected.
                        (Check that the _references.bib and _citations.bib files
                        for @RWebberBurrows2018 are still in the bib_files folder)"""
        
        print(result)
        return result

    def pdf_reader(self):
        """
        Tests that reader.py is able to read and interpret .pdf files by 
        running a check on the pdf file of references for @RWebberBurrows2018.
        """
        
        self.tests += 1

        try:
            db_file = os.path.join(sys.path[0], 'citation_graph.db')
            get = reader.Pdf(db_file, 'RWebberBurrows2018')
            data = get.refs()
            assert len(data) == 216
            self.success += 1
            result = "\nTest Successful: PDF Reader working as expected."
        except:
            e = sys.exc_info()
            print(f"\n\n\nERROR: {e}")
            result = "\nTest Failed: PDF Reader not working as expected."
        
        print(result)
        return result
                
    def api_interactions(self):
        """
        Tests that the DOI & OCI APIs are working by testing for doi='10.1186/ar4086'.
        """
        
        self.tests += 1

        try:
            get = reader.Api('10.1186/ar4086')
            responses = get.data()
            for r in responses: assert r.status_code == 200
            self.success += 1
            result = "\nTest Successful: DOI & OCI API interactions working as expected."
        except:
            e = sys.exc_info()
            print(f"\n\n\nERROR: {e}")
            result = "\nTest Failed: DOI & OCI API interactions not working as expected."
        
        print(result)
        return result
        
    def lit_classes(self):
        """
        Tests that the literature.py classes are working.
        """
        
        self.tests += 1

        db_file=os.path.join(sys.path[0], 'citation_graph.db')

        details = ""


        try:
            test_text = lit.Text(db_file, key='TEST_TEXT')
            test_text.remove()
            details += "\n>>>lit.Text() class working"
            test_book = lit.Book(db_file, key='TEST_BOOK')
            test_book.remove()
            details += "\n>>>lit.Book() class working"
            test_chapter = lit.Chapter(db_file, key='TEST_CHAPTER')
            test_chapter.remove()
            details += "\n>>>lit.Chapter() class working"
            test_article = lit.Article(db_file, key='TEST_ARTICLE')
            test_article.remove()
            details += "\n>>>lit.Article() class working"
            test_creator = lit.Creator(db_file, surname='TEST_CREATOR')
            test_creator.remove()
            details += "\n>>>lit.Creator() class working"
            test_citation = lit.Citation(db_file, citing='TEST_CITATION', cited='TEST_REFERENCE')
            test_citation.remove()
            details += "\n>>>lit.Citation() class working"
            
            self.success += 1
            result = "\nTest Successful: Literature Classes working as expected."
            
        except:
            e = sys.exc_info()
            print(f"\n\n\nERROR: {e}")
            result = "\nTest Failed: Literature Classes not working as expected."
            result += details
        
        print(result)
        return result



if __name__ == '__main__':
    Test()
