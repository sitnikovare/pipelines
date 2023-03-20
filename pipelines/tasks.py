import csv

import pandas as pd
import sqlite3
from .dbmanager import DBmanager

class BaseTask:
    """Base Pipeline Task"""

    def __init__(self):
        self.table_object = None
        self.table_object_norm = None

    def safe_table_object(self, object_from_loader):
        self.table_object = object_from_loader
        return self.table_object

    def run(self):
        raise RuntimeError('Do not run BaseTask!')

    def short_description(self):
        pass

    def __str__(self):
        task_type = self.__class__.__name__
        return f'{task_type}: {self.short_description()}'


class CopyToFile(BaseTask):
    """Copy table data to CSV file"""

    def __init__(self, table, output_file):
        self.table = table
        self.output_file = output_file + ".csv"

    def short_description(self):
        return f'{self.table} -> {self.output_file}'

    def run(self):
        print(f"Copy table `{self.table}` to file `{self.output_file}`")
        # BaseTask.table_object_norm.to_csv("output/" + self.output_file, index=False)
        dbm = DBmanager("sqlite_080323.db")
        dbm.load_table_to_file(self.table, self.output_file)


class LoadFile(BaseTask):
    """Load file to table"""

    def __init__(self, table, input_file):
        self.table_name = None
        self.table = table
        self.input_file = input_file

    def short_description(self):
        return f'{self.input_file} -> {self.table}'

    def run(self):
        print(f"Load file `{self.input_file}` to table `{self.table}`")
        self.table_name = self.table
        self.table = pd.read_csv(self.input_file)
        BaseTask.safe_table_object(BaseTask, self.table)
        # print("Table shape:", self.table.shape)
        dbm = DBmanager("sqlite_080323.db")
        dbm.create_table_from_csv(BaseTask.table_object, self.table_name)



class RunSQL(BaseTask):
    """Run custom SQL query"""

    def __init__(self, sql_query, title=None):
        self.title = title
        self.sql_query = sql_query

    def short_description(self):
        return f'{self.title}'

    def run(self):
        print(f"Run SQL ({self.title}):\n{self.sql_query}")
        dbm = DBmanager("sqlite_080323.db")
        dbm.execute_query(self.sql_query)


def domain_of_url_old(data):
    data['domain_of_url'] = data['url'].replace(to_replace='^https?:\/\/', value='', regex=True)
    return data


class CTAS(BaseTask):
    """SQL Create Table As Task"""

    def __init__(self, table, sql_query, title=None):
        self.table = table
        self.sql_query = sql_query
        self.title = title or table

    def short_description(self):
        return f'{self.title}'

    def run(self):
        create_query = f"Create table IF NOT EXISTS {self.table} as {self.sql_query}"
        print(create_query)
        # BaseTask.table_object_norm = domain_of_url_old(BaseTask.table_object)
        dbm = DBmanager("sqlite_080323.db")
        dbm.execute_query(create_query)
        # dbm.create_table_from_csv(BaseTask.table_object_norm, self.table)
