import sqlite3


class DBmanager:

    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = self.connect()
        self.close()

    def test_in_module(self):
        print("DBMANAGER RUNNING")
        query = "INSERT INTO test_table (message) VALUES (\"test module PIPELINES\")"
        print(query)
        execute_query(query)
    def connect(self):
        try:
            connection_line = 'D:\CSIT\Sem8_Pipelines\pipelines\pipelines\dbmanager\database\\' + self.db_file
            sqlite_connection = sqlite3.connect(connection_line)
            cursor = sqlite_connection.cursor()
            print("DBMANAGER_INFO: Connection successfully opened")

            sqlite_select_query = "select sqlite_version();"
            cursor.execute(sqlite_select_query)
            record = cursor.fetchall()
            print("DBMANAGER_INFO: SQLite DB version: ", record)
            cursor.close()

        except sqlite3.Error as error:
            print("DBMANAGER_ERROR:", error)

        return sqlite_connection

    def close(self,):
        self.connection.close()
        print("DBMANAGER_INFO: Connection to SQLite closed")

    def execute_query(self, sql_query):
        try:
            print("DBMANAGER_INFO: SQL query - ", sql_query)
            cursor = self.connection.cursor()
            cursor.execute(sql_query)
            self.connection.commit()
            print(cursor.fetchall())
            cursor.close()

        except sqlite3.Error as error:
            print("DBMANAGER_ERROR: ", error)

dbm = DBmanager("sqlite_080323.db")
# dbm.connect()
# dbm.execute_query("SELECT * FROM connections_recorder")
# dbm.close()