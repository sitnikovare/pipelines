import pandas as pd
import sqlite3

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
        BaseTask.table_object_norm.to_csv("output/" + self.output_file, index=False)


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


def domain_of_url(data):
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
        print(f"Create table `{self.table}` as SELECT:\n{self.sql_query}")
        BaseTask.table_object_norm = domain_of_url(BaseTask.table_object)
        dbm = DBmanager("sqlite_080323.db")
        dbm.create_table_from_csv(BaseTask.table_object_norm, self.table)

class DBmanager:

    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = self.connect()
        self.close()

    def connect(self):
        try:
            connection_line = 'D:\CSIT\Sem8_Pipelines\pipelines\pipelines\dbmanager\database\\' + self.db_file
            sqlite_connection = sqlite3.connect(connection_line)
            cursor = sqlite_connection.cursor()
            # print("DBMANAGER_INFO: Connection successfully opened")

            # sqlite_select_query = "select sqlite_version();"
            # cursor.execute(sqlite_select_query)
            # record = cursor.fetchall()
            # print("DBMANAGER_INFO: SQLite DB version: ", record)
            cursor.close()

        except sqlite3.Error as error:
            print("DBMANAGER_ERROR:", error)

        return sqlite_connection

    def close(self,):
        self.connection.close()
        # print("DBMANAGER_INFO: Connection to SQLite closed")

    def execute_query(self, sql_query):
        try:
            # print("DBMANAGER_INFO: SQL query - ", sql_query)
            self.connection = self.connect()
            cursor = self.connection.cursor()
            cursor.execute(sql_query)
            self.connection.commit()
            # print(cursor.fetchall())
            cursor.close()
            self.close()

        except sqlite3.Error as error:
            print("DBMANAGER_ERROR: ", error)


    def create_table_from_csv(self, csv_table, table_name):
        cols = csv_table.columns
        cols_info = ""
        cols_str = ""
        for col in cols[:len(cols)-1]:
            cols_info += col + " TEXT,"
            cols_str += col + ", "
        cols_info += cols[-1] + " TEXT"
        cols_str += cols[-1]
        query_create_table = "CREATE TABLE " + table_name + " (" + cols_info + ")"
        # print("DBMANAGER_INFO: SQL query - ", query_create_table)
        self.execute_query(query_create_table)

        for rowIndex, row in csv_table.iterrows():
            query_insert = "INSERT INTO " + table_name + " (" + cols_str + ") VALUES ("
            cur_values = ""
            for columnIndex, value in row.items():
                if columnIndex == cols[-1]:
                    break
                cur_values += "\'" + str(value) + "\',"
            query_insert += cur_values + "\'" + row[-1] + "\')"
            # print("DBMANAGER_INFO: SQL query - ", query_insert)
            self.execute_query(query_insert)
