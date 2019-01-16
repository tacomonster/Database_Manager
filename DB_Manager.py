import sqlite3
from sqlite3 import OperationalError, IntegrityError
import os

"""
YouTube: https://youtu.be/GdNA6AFk0Mg
"""

class DB_Manager:

    conn = None

    def __init__(self, db_name, dict_output=False):
        self.db_name = db_name
        self.dict_output = dict_output

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        # Query output for list of dictionaries
        if self.dict_output:
            self.conn.row_factory = sqlite3.Row
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def create_table(self, sql_tables_file):
        """Creates table in DB from a script file"""
        with open(sql_tables_file, 'r') as f:
            try:
                self.conn.executescript(f.read())
            except OperationalError:
                pass

    def insert_row(self, table_name, **kwargs):
        """
        Inserts a row into a specified table.
        :param string table_name: name of table in DB
        :param dict **kwargs: dictionary key values of table column names and values
        """
        sql = """INSERT INTO {tbl} {col} VALUES {val};
              """.format(tbl=table_name,
                         col=tuple(kwargs.keys()),
                         val=tuple(kwargs.values())
                         )
        try:
            self.conn.cursor().execute(sql)
            self.conn.commit()
        except IntegrityError:
            print('ERROR: Unique Value already exists in DB.')

    def get_rows(self, table_name, param='1=1', fetch_last=False):
        """
        Returns rows from table
        :param string table_name: name of table in DB
        :param string param: conditional parameter to retreive row data
        :param bool fetch_last: returns last item added to table
        """
        param = param if type(param) is not list else \
            ' AND '.join([x for x in param])

        sql = """SELECT * FROM {} WHERE {};
              """.format(table_name, param)

        try:
            c = self.conn.cursor().execute(sql)
            # Dictionary output option
            if self.dict_output:
                query = [dict(row) for row in c.fetchall()]
            else:
                query = c.fetchall()
            # Last item in query
            if fetch_last:
                return query[-1]
            return query

        # When SQL Query is broken
        except OperationalError:
            raise (OperationalError("Cannot Execute SQL Query: %s" % sql))
            
    def update_row(self, table_name, col, new_val, where='1=1'):
        """Updating an existing row"""
        sql = """UPDATE {}
                 SET {col} = {nv}
                 WHERE {w};
              """.format(table_name, col=col, nv=new_val, w=where)
        self.conn.cursor().execute(sql)
        self.conn.commit()


if __name__ == '__main__':
    DB = '.{}lalala.sqlite'.format(os.sep)
    tables_script = '.{}tables.sql'.format(os.sep)
    with DB_Manager(DB, dict_output=True) as mngr:
        mngr.create_table(tables_script)
        v = {'first_name': 'hander',
             'last_name': 'taco',
             'email': 'hander@taco.com5',
             'phone': '123-456-8578'}
        mngr.insert_row(table_name='contacts', **v)
        print(mngr.get_rows('contacts', param=['first_name LIKE "hander"', 'contact_id > 3']))
        # print(mngr.get_rows('contacts', 'contact_id > 1', fetch_last=True))


"""
Terminal display commands
.header on
.mode columns
WHERE Clause Reference: https://www.tutorialspoint.com/sqlite/sqlite_where_clause.htm
"""
