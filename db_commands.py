import sqlite3

db = 'citation_graph.db'

def connect(db):
    def wrapper(func):
        def connected_function(*args, **kwargs):
            conn = sqlite3.connect(db)
            c = conn.cursor()
            print('connected!')
            process = func(*args, **kwargs)
            conn.commit()
            conn.close()
            print('connection closed')
            return process
        return connected_function
    return wrapper

@connect(db)
def create_table(name, columns, db=db):
    """
    Creates a table.
    
    Args:
        name (string)
        columns (tuple of strings)
        db (string): name of the database file 
                    -- if none, it will create it.
    """
    print('creating table')
    c.execute(f'''CREATE TABLE {name}
             {columns}''')
    print('created table')

@connect(db)
def save_row_to_table(table, row):
    """
    Saves row of data to table.
    
    Args:
        data (list)
    """
    question_marks = ('?,' * len(row))[0:-1] # slice to remove trailing comma
    c.executemany(f"INSERT INTO {table} VALUES ({question_marks});", (row,))
    print(f"Row saved to table '{table}' in database '{db}': {row}")


@connect(db)
def search(table, column, value):
	pass
	





if __name__ == '__main__':
    conn = sqlite3.connect('citation_graph.db')
    c = conn.cursor()
    
    text_columns = ('key', 'type')
    book_columns = ('key', 'publication_year', 'title', 'publisher', 'location', 'number_of_pages')
    chapter_columns = ('key', 'title', 'pages', 'book_key')
    article_columns = ('key', 'publication_year', 'title', 'journal', 'volume', 'edition', 'pages')
    creator_columns = ('surname', 'initial', 'year_of_birth', 'year_of_death')
    text_creator_columns = ('key', 'creator_key', 'creator_ordinal')
    
    # ~ create_table('texts', text_columns)
    # ~ create_table('books', book_columns)
    # ~ create_table('chapters', chapter_columns)
    # ~ create_table('articles', article_columns)
    # ~ create_table('creators', creator_columns)
    # ~ create_table('text_creator', text_creator_columns)

    save_row_to_table('texts', ('RWebberBurrows2018', 'book'))
    save_row_to_table('chapters', ('Key', 'A Title', '13-15', 'RWebberBurrows2018'))
