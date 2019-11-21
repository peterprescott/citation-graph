import sqlite3  #db functionality ~ https://docs.python.org/3/library/sqlite3.html
import string

class Query():

    def __init__(self, db_filename):
        self.db = db_filename
        
    def open(self):
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()
        
    def close(self):
        self.conn.commit()
        self.conn.close()
                
    def test_connection(self):
        """Shows that tests are successfully importing db_commands"""
        print("connected")
        return "connected"

    def create_table(self, table, columns):
        """
        Creates a table.
        
        Args:
            table (string)
            columns (tuple of strings)
            c: database connection.
        """

        self.open()
        print('creating table')
        self.c.execute(f'''CREATE TABLE {table} {columns}''')
        print('created table')
        self.close()
        
    
    def drop_table(self, table):
        """
        Drops table.
        
        Args:
            table (string)
            c: database connection.
        """
        
        self.open()
        print(f"dropping table '{table}'")
        self.c.execute(f'''DROP TABLE {table}''')
        self.conn.close()

    def save_row_to_table(self, table, row, allow_duplicate=False):
        """
        Saves row of data to table.
        
        Args:
            data (list)
        """
        
        self.open()
        print('...saving row to table...')
        
        if allow_duplicate == False:
            # check if duplicate already exists
            if self.search(table, 'key', row[0]):
                print(f'ERROR in trying to save {row} to {table}: row already added!')
                return {'status':'error','error':'key already exists'}
        
        question_marks = ('?,' * len(row))[0:-1] # slice to remove trailing comma
        self.c.executemany(f"INSERT INTO {table} VALUES ({question_marks});", (row,))
        self.close()
        print(f"Row saved to table '{table}' in database '{self.db}': {row}")
        return {'status':'successful'}

    def search(self, table, column, value, with_rowid=False):
        """
        Searches column in table for specified value.
        
        Args:
            table (string)
            column (string)
            value
            c: database connection
            with_rowid (Boolean)
        """
        
        self.open()
        print(f'searching for value "{value}" in column "{column}" of table "{table}"')
        if with_rowid==True:
            self.c.execute(f"SELECT rowid, * FROM {table} WHERE {column}=?", (value,))
        else:
            self.c.execute(f"SELECT * FROM {table} WHERE {column}=?", (value,))
        search_results = self.c.fetchall()
        print(search_results)
        return search_results

    def remove_row(self, table, rowid):
        """
        Removes specified row from table.
        
        Args:
            table (string)
            rowid (int)
            c: database connection
        """
        
        self.open()
        print('removing row {rowid} from {table}')
        self.c.execute(f"DELETE FROM {table} WHERE rowid=?", (rowid,))
        self.close()

    def remove_duplicate_rows(self, table, repeated_value, all_but=1, column='key'):
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
        
        while len(self.search(table, column, repeated_value, with_rowid=True)) > all_but:
            self.remove_row(table, self.search(table, column, repeated_value, with_rowid=True)[1][0])



if __name__ == '__main__':
    
    text_columns = ('key', 'publication_year', 'title', 'type')
    book_columns = ('key', 'publisher', 'location', 'number_of_pages')
    chapter_columns = ('key', 'pages', 'book_key')
    article_columns = ('key', 'journal', 'volume', 'edition', 'pages')
    creator_columns = ('key', 'surname', 'initial')
    text_creator_columns = ('key', 'text_key', 'creator_key', 'creator_role', 'creator_ordinal')
    citation_columns = ('key', 'citing_key', 'cited_key')
    
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

