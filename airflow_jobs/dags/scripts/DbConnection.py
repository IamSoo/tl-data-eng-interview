__author__ = 'Soonam Kalyan'

"""
A class creates a connection object and handles the storage
"""
import os
from sqlalchemy import create_engine
import psycopg2


class DbConnection(object):
    """docstring for DbConnection"""

    def __init__(self):
        self.username = os.getenv('POSTGRES_USER', 'postgres')
        self.password = os.getenv("POSTGRES_PASSWORD",'postgres')
        self.db = os.getenv("POSTGRES_DB", 'postgres')
        self.port = os.getenv("POSTGRES_PORT", '5432')
        #print(f'postgresql://{self.username}:{self.password}@postgres_local:{self.port}/{self.db}')
        self.engine = create_engine(f'postgresql://{self.username}:{self.password}@postgres_local:5432/{self.db}')

    def get_db_engine(self):
        return self.engine

    def save_df_to_table(self, df, table, engine):
        ## Save data to db
        connection = engine.connect()
        try:
            connection.execute(f'DROP TABLE IF EXISTS {table};')
            df.to_sql(table, connection)
        except:
            connection.close()
        finally:
            connection.close()
