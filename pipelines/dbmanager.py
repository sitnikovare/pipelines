import sqlite3
import os
import csv
import re

def domain_of_url(str_s):
    return re.sub('\/.*', '', re.sub('^https?:\/\/', '', str_s))

class DBmanager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = self.connect()
        self.connection.create_function("domain_of_url", 1, domain_of_url)
        self.close()

    def connect(self):
        try:
            # dbpath = os.path.abspath("../pipelines/database/" + self.db_file)
            dbpath = os.path.abspath("pipelines/database/" + self.db_file)
            # print(dbpath)
            sqlite_connection = sqlite3.connect(dbpath)
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
            self.connection.create_function("domain_of_url", 1, domain_of_url)
            self.connection.execute(sql_query)
            self.connection.commit()
            # print(cursor.fetchall())
            # cursor.close()
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
        query_create_table = "CREATE TABLE IF NOT EXISTS " + table_name + " (" + cols_info + ")"
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

    def load_table_to_file(self, table, file):
        self.connection = self.connect()
        sql_query = f"SELECT * from {table};"
        cursor = self.connection.cursor()
        cursor.execute(sql_query)
        filepath = "output/" + file
        with open(filepath, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])
            csv_writer.writerows(cursor.execute(sql_query))
        cursor.close()
        self.close()
