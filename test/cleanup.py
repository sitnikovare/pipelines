import os
from pipelines.dbmanager import *

def cleanup_after_tests():
    os.remove("output/norm_test.csv")
    dbm = DBmanager("sqlite_080323.db")
    connection = dbm.connect()
    select_query = "drop table original_test"
    cursor = connection.cursor()
    cursor.execute(select_query)
    cursor.close()
    connection.close()

cleanup_after_tests()