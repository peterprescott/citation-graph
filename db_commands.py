from supersqlite import sqlite3

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
    """
    print('creating table')
    c.execute(f'''CREATE TABLE {name}
             {columns}''')
    print('created table')

           
def save_row_to_db(row, db=db):
    """
    Saves row of data to table.
    
    Args:
        data (list)
    """

    try:
        c.executemany("INSERT INTO ? VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", 
            (row,))
        print(f"Row saved to database: {row}")
    except:
        print(f"Row NOT saved to database: {row}")

def search(table, column, value):
	pass
	





if __name__ == '__main__':
    conn = sqlite3.connect('citation_graph.db')
    c = conn.cursor()
    
    text_columns = ('Key', 'Type')
    book_columns = ('Key', 'Year')
    chapter_columns = ('Key', ...)
    article_columns = ('Key', ...)
    person_columns = ('Surname', 'Initial')
    text_creators = ('Key', 'PersonKey', 'Person_Ordinal')
    
    
    create_table('Books', book_columns)
    

    conn.commit()
    conn.close()
