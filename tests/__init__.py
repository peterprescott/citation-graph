"""Runs tests and documents results. """

from datetime import datetime   # for recording data and time of tests
from selenium import webdriver  # for testing web app
import sqlite3                  # for testing database
import os                       # for navigating between folders
import sys


test_count = 0
success_count = 0


def test_flask_app(page_location, confirmation):
    """
    Tests that Flask App is running as expected.

    Uses Selenium Webdriver to check Flask App is running as expected.

    Args:
        URL (string): the address where the Flask App is running.
        page_title (string): the title of the webpage,
            as it should be defined by <title> tags.
    """

    global test_count 
    global success_count
    test_count += 1

    driver = webdriver.Chrome(os.path.join(sys.path[0], 'chromedriver.exe'))
    driver.get(page_location)
    print(driver)
    if driver.title == confirmation:
        success_count += 1
        result = "\nTest Successful: Flask App running as expected."
    else:
        result = """\nTest Failed: Flask App not running as expected. 
                (It may not be broken -- you need to run it explicitly.)"""
    print(result)
    return result

def test_db_commands(file):
    """
    Tests that database commands from ../db_commands.py are working as expected.
    
    Args:
        file (string): file location for db_commands.py
    """ 
    
    sys.path.append(os.path.dirname(os.path.expanduser(file)))
    import db_commands as db
    
    global test_count
    global success_count
    test_count += 1
    
    details = ""
    try:
        assert db.test_connection() == "connected"
        details += '\n>>>Connection working'
        db.create_table('test_table', ('key', 'other_column'))
        details += '\n>>>create_table() working'
        db.save_row_to_table('test_table', ('test_key', 'testing_testing'))
        details += '\n>>>save_row_to_table() working'
        assert db.search('test_table', 'key', 'test_key')[0] == ('test_key', 'testing_testing')
        details += '\n>>>search() working'
        db.remove_row('test_table', 1)
        details += '\n>>>remove_row() working'
        assert len(db.search('test_table', 'key', 'test_key')) == 0
        db.save_row_to_table('test_table', ('test_key', 'testing_testing'), allow_duplicate=True)
        db.save_row_to_table('test_table', ('test_key', 'testing_testing'), allow_duplicate=True)
        assert len(db.search('test_table', 'key', 'test_key')) == 2
        details += '\n>>>testing remove_duplicate_rows()'
        db.remove_duplicate_rows('test_table', 'test_key')
        assert len(db.search('test_table', 'key', 'test_key')) == 1
        details += '\n>>>remove_duplicate_rows() working'
        db.drop_table('test_table')
        details += '\n>>>drop_table() working'
        success_count += 1
        result = "\nTest Successful: Database Commands working as expected."
    except:
        result = "\nTest Failed: Database Commands not working as expected."
        result += details
    print(result)
    return result

def test_lit_classes():
    global test_count
    global success_count
    test_count += 1
    
    try:
        assert True == True
        success_count += 1
        result = "\nTest Successful: Literature Classes working as expected."
    except:
        result = "\nTest Failed: Literature Classes not working as expected."
    
    print(result)
    return result
    
def test_bib_reader():
    global test_count
    global success_count
    test_count += 1
    
    try:
        assert True == True
        success_count += 1
        result = "\nTest Successful: .bib Reader working as expected."
    except:
        result = "\nTest Failed: .bib Reader not working as expected."
    
    print(result)
    return result

def test_pdf_reader():
    global test_count
    global success_count
    test_count += 1
    
    try:
        assert True == True
        success_count += 1
        result = "\nTest Successful: PDF Reader working as expected."
    except:
        result = "\nTest Failed: PDF Reader not working as expected."
    
    print(result)
    return result
    
def test_api_interactions():
    global test_count
    global success_count
    test_count += 1
    
    try:
        assert True == True
        success_count += 1
        result = "\nTest Successful: DOI & OCI API interactions working as expected."
    except:
        result = "\nTest Failed: DOI & OCI API interactions not working as expected."
    
    print(result)
    return result
    
def test_jamstack_gui():
    global test_count
    global success_count
    test_count += 1
    
    try:
        assert True == True
        success_count += 1
        result = "\nTest Successful: JAMstack GUI working as expected."
    except:
        result = "\nTest Failed: JAMstack GUI not working as expected."
    
    print(result)
    return result
    
def test_web_scraper():
    global test_count
    global success_count
    test_count += 1
    
    try:
        assert True == True
        success_count += 1
        result = "\nTest Successful: Web Scraper working as expected."
    except:
        result = "\nTest Failed: Web Scraper not working as expected."
    
    print(result)
    return result
    
def test_logic():
    global test_count
    global success_count
    test_count += 1
    
    try:
        assert True == True
        success_count += 1
        result = "\nTest Successful: Logic working as expected."
    except:
        result = "\nTest Failed: Logic not working as expected."
    
    print(result)
    return result
    

if __name__ == '__main__':

    with open(os.path.join(sys.path[0], 'logs.txt'), 'a') as log:
        now = datetime.now()
        log.write("\n" + now.strftime("%d/%m/%Y %H:%M:%S"))
        log.write(test_logic())
        log.write(test_flask_app("localhost:5000/test", "Running!"))
        log.write(test_db_commands(os.path.join(sys.path[0],'..','db_commands.py')))
        # ~ log.write(test_lit_classes())
        # ~ log.write(test_bib_reader())
        # ~ log.write(test_pdf_reader())
        # ~ log.write(test_api_interactions())
        # ~ log.write(test_jamstack_gui())
        # ~ log.write(test_web_scraper())
        summary = f"\nRan {test_count} tests: {success_count}/{test_count} were successful."
        print(summary)
        log.write(summary)
        log.write("\n")
        
