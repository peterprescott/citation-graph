import sqlite3  #db functionality ~ https://docs.python.org/3/library/sqlite3.html
import string
import os.path
import sys

class Query():

    def __init__(self, db_filename):
        self.db = db_filename
        
    def open(self):
        """
        Opens connection to database.
        """
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()
        
    def close(self):
        """
        Commits changes and closes connection to database.
        """
        self.conn.commit()
        self.conn.close()
                
    def test(self):
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
        
        return search_results
        
    def full(self, table):
        """
        Shows full table.
        
        Args:
            table (string)
        """
        
        self.open()
        self.c.execute(f"SELECT rowid, * FROM {table}")
        full_results = self.c.fetchall()
        print(f"Returning full results for {table} table.")
        return full_results

    def remove_row(self, table, rowid):
        """
        Removes specified row from table.
        
        Args:
            table (string)
            rowid (int)
            c: database connection
        """
        
        self.open()
        print(f'removing row {rowid} from {table}')
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
            self.remove_row(table, self.search(table, column, repeated_value, with_rowid=True)[all_but][0])
    
    def reboot(self):
        """
        Create necessary tables for Literature classes.
        """
        text_columns = ('key', 'publication_year', 'title', 'type', 'doi')
        book_columns = ('key', 'publisher', 'location', 'number_of_pages', 'isbn')
        chapter_columns = ('key', 'pages', 'book_key')
        article_columns = ('key', 'journal', 'volume', 'edition', 'pages')
        creator_columns = ('key', 'surname', 'initial')
        text_creator_columns = ('key', 'text_key', 'creator_key', 'creator_role', 'creator_ordinal')
        citation_columns = ('key', 'citing_key', 'cited_key')
        
        self.create_table('texts', text_columns)
        self.create_table('books', book_columns)
        self.create_table('chapters', chapter_columns)
        self.create_table('articles', article_columns)
        self.create_table('creators', creator_columns)
        self.create_table('text_creators', text_creator_columns)
        self.create_table('citations', citation_columns)
        
    def follow_edges(self, text_key, direction = "cited", full_node_list=[], full_edge_list=[], iteration=1):
        """Helper function to get outgoing edges from text and connected nodes."""

        
        new_nodes = []
        
        citations = self.search("citations", f"{direction}_key", text_key)
        for citation_row in citations:
            if direction == "cited": 
                other_key = citation_row[1]
                group_colour = iteration
            else: 
                other_key = citation_row[2]
                group_colour = iteration * -1
            full_edge_list.append(dict(source = text_key, target = other_key, value = 1))

            node_data = self.search("texts", "key", other_key)
            if node_data:
                node_row = node_data[0] # data returned by query as list of tuples
                other_title = node_row[2] #.replace(':','--').replace('"','').replace("'",'')
                other_type = node_row[3]
                new_node = dict(id = other_key, title = other_title, type = other_type, group = group_colour)
                full_node_list.append(new_node)
                new_nodes.append(new_node)
                
        return new_nodes
    
    def json_graph(self, text_key, radius=1):
        """
        Returns nodes and edges for JSON citation graph centred on specified text.
        
        text_key (string): in BetterBibTex format [authForeIni][authEtAl][year].
        radius (int): **TODO** degrees of separation between focal text and others included.
        """
        
        node_list = []
        edge_list = []

        # get data for the text
        node_data = self.search("texts", "key", text_key)
        if node_data:
                node_row = node_data[0] # data returned by query as list of tuples
                text_title = node_row[2].replace(':','--').replace('"','').replace("'",'')
                text_type = node_row[3]
                node_list.append(dict(id = text_key, title = text_title, type = text_type, group = 1))
        
        next_nodes = [{'id':text_key}]
        iteration = 1
        while iteration <= radius:
            new_nodes = next_nodes
            next_nodes = []
            for node in new_nodes:
                citing_nodes = self.follow_edges(node['id'], "cited", node_list, edge_list, iteration)
                for citing_node in citing_nodes: next_nodes.append(citing_node)
                cited_nodes = self.follow_edges(node['id'], "citing", node_list, edge_list, iteration)
                for cited_node in cited_nodes:  next_nodes.append(cited_node)
                new_nodes.remove(node)
                iteration = iteration + 1
        
        
        graph = {"nodes": node_list, "links": edge_list}
        print(graph)
        return graph
        

if __name__ == '__main__':
    
    q = Query(os.path.join(sys.path[0], 'citation_graph.db'))
    # ~ q.reboot()

    # ~ for row in q.full('texts'): print(row)
    # ~ for row in q.full('books'): print(row)
    # ~ for row in q.full('chapters'): print(row)
    # ~ for row in q.full('articles'): print(row)
    # ~ for row in q.full('creators'): print(row)
    # ~ for row in q.full('text_creators'): print(row)
    edge_list = []
    
    text_key = 'RWebberBurrows2018'
    print(q.json_graph(text_key))
