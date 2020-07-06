# This file was adapted from http://www.postgresqltutorial.com/postgresql-python/connect/

# The following config() function reads in the database.ini file and returns the connection
# parameters as a dictionary. This function will be imported in to the main python script:
import psycopg2
import os
from configparser import ConfigParser


class DB:
    CONFIG = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials', 'database.ini')

    def __init__(self):
        config = self.get_config(self.CONFIG)
        self._conn = psycopg2.connect(**config)
        self._conn.set_session(autocommit=True)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        self.__init__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.close()

    # def commit(self):
    #     return self._conn.commit()

    @property
    def cursor(self):
        return self._cursor

    @staticmethod
    def get_config(filename: str, section='postgresql') -> dict:
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)
        db = {}

        # Checks to see if section (postgresql) parser exists
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]

        # Returns an error if a parameter is called that is not listed in the initialization file
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db

    def run_sql(self, sql: str) -> None:

        # # Establish a connection to the database by creating a cursor object
        #
        # # Obtain the configuration parameters
        # params = self.config()
        # # Connect to the PostgreSQL database
        # conn = psycopg2.connect(**params)
        # # Create a new cursor
        # cur = conn.cursor()
        #
        # def create_pandas_table(sql_query, database=conn) -> pandas.DataFrame:
        #     table = pandas.read_sql_query(sql_query, database)
        #     return table
        #
        # response = create_pandas_table(sql, conn)
        # # Close the cursor and connection to so the server can allocate
        # # bandwidth to other requests
        # cur.close()
        # conn.close()
        #
        # return response
        pass
