import sqlite3  #db functionality ~ https://docs.python.org/3/library/sqlite3.html
import string

db = 'citation_graph.db'

def connect(db):
    """
    Decorates function with database connection.
    
    Args:
        db (string): filename of database (will be created if non-existent).
    """
    def wrapper(func):
        def connected_function(*args, **kwargs):
            """See source code. 
            Sphinx doesn't straightforwardly autodocument decorated functions..."""

            conn = sqlite3.connect(db)
            c = conn.cursor()
            print(f'connected to {db}.')
            process = func(*args, **kwargs, c=c)
            conn.commit()
            conn.close()
            print('connection closed.')
            return process
        return connected_function
    return wrapper
    
def test_connection():
    """Shows that tests are successfully importing db_commands"""
    print("connected")
    return "connected"

@connect(db)
def create_table(table, columns, c):
    """
    Creates a table.
    
    Args:
        table (string)
        columns (tuple of strings)
        c: database connection.
    """
    print('creating table')
    c.execute(f'''CREATE TABLE {table}
             {columns}''')
    print('created table')

@connect(db)
def drop_table(table, c):
    """
    Drops table.
    
    Args:
        table (string)
        c: database connection.
    """
    print(f"dropping table '{table}'")
    c.execute(f'''DROP TABLE {table}''')

@connect(db)
def save_row_to_table(table, row, c, allow_duplicate=False):
    """
    Saves row of data to table.
    
    Args:
        data (list)
    """
    print('...saving row to table...')
    
    if allow_duplicate == False:
        # check if duplicate already exists
        if search(table, 'key', row[0]):
            print(f'ERROR in trying to save {row} to {table}: row already added!')
            return {'status':'error','error':'key already exists'}
    
    question_marks = ('?,' * len(row))[0:-1] # slice to remove trailing comma
    c.executemany(f"INSERT INTO {table} VALUES ({question_marks});", (row,))
    print(f"Row saved to table '{table}' in database '{db}': {row}")
    return {'status':'successful'}

@connect(db)
def search(table, column, value, c, with_rowid=False):
    """
    Searches column in table for specified value.
    
    Args:
        table (string)
        column (string)
        value
        c: database connection
        with_rowid (Boolean)
    """
    print(f'searching for value "{value}" in column "{column}" of table "{table}"')
    if with_rowid==True:
        c.execute(f"SELECT rowid, * FROM {table} WHERE {column}=?", (value,))
    else:
        c.execute(f"SELECT * FROM {table} WHERE {column}=?", (value,))
    search_results = c.fetchall()
    print(search_results)
    return search_results

@connect(db)
def remove_row(table, rowid, c):
    """
    Removes specified row from table.
    
    Args:
        table (string)
        rowid (int)
        c: database connection
    """
    print('removing row {rowid} from {table}')
    c.execute(f"DELETE FROM {table} WHERE rowid=?", (rowid,))

@connect(db)
def remove_duplicate_rows(table, repeated_value, c, column='key'):
    """
    Removes rows with specified duplicate value.
    
    Args:
        table (string)
        repeated_value
        c: database connection
        column (string): default is 'key' which will only remove duplicate rows,
                        but any column could be specified to remove all rows 
                        with duplicate values.
    """
    while len(search(table, column, repeated_value, with_rowid=True)) > 1:
        remove_row(table, search(table, column, repeated_value, with_rowid=True)[1][0])



if __name__ == '__main__':
    
    text_columns = ('key', 'type')
    book_columns = ('key', 'publication_year', 'title', 'publisher', 'location', 'number_of_pages')
    chapter_columns = ('key', 'title', 'pages', 'book_key')
    article_columns = ('key', 'publication_year', 'title', 'journal', 'volume', 'edition', 'pages')
    creator_columns = ('key', 'surname', 'initial', 'year_of_birth', 'year_of_death')
    text_creator_columns = ('key', 'creator_key', 'creator_ordinal')
    
    # ~ create_table('texts', text_columns)
    # ~ create_table('books', book_columns)
    # ~ create_table('chapters', chapter_columns)
    # ~ create_table('articles', article_columns)
    # ~ create_table('creators', creator_columns)
    # ~ create_table('text_creator', text_creator_columns)

    # ~ save_row_to_table('texts', ('RWebberBurrows2018', 'book'), allow_duplicate=True)
    # ~ save_row_to_table('chapters', ('Key', 'A Title', '13-15', 'RWebberBurrows2018'))
    
    # ~ save_row_to_table('texts', ('anotherkey', 'book'))
    # ~ save_row_to_table('texts', ('andanotherkey', 'book'))    
    
    
    # ~ remove_duplicate_rows('chapters', '')


    remove_duplicate_rows('texts', 'book', column='type')

    eg = search('texts', 'type', 'book')
    print(eg)

