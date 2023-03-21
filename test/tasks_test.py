from pipelines.tasks import *
from pipelines.dbmanager import *
import pandas as pd
import pytest

base_task = BaseTask()
def test_loadFileTask():
    table_name = 'original_test'
    file_path = 'original/original_test.csv'

    load_task = LoadFile(input_file=file_path, table=table_name)
    load_task.run()

    dbm = DBmanager("sqlite_080323.db")
    connection = dbm.connect()
    select_query = f"SELECT * from {table_name}"
    cursor = connection.cursor()
    cursor.execute(select_query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    assert result[0][2] == "http://hello.com/hello"

def test_CTASTask():
    table_name = 'norm_test'
    ctas_task = CTAS(
        table=table_name,
        sql_query='''
            select *, domain_of_url(url)
            from original_test;
        ''')
    ctas_task.run()

    dbm = DBmanager("sqlite_080323.db")
    connection = dbm.connect()
    select_query = f"SELECT * from {table_name}"
    cursor = connection.cursor()
    cursor.execute(select_query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    assert result[0][3] == "hello.com"

def test_CopyTask():
    table_name = 'norm_test'
    copy_task = CopyToFile(table=table_name,output_file='norm_test')
    copy_task.run()

    result_file = pd.read_csv(f"output/{table_name}.csv")
    assert result_file.iloc[0]['domain_of_url(url)'] == "hello.com"

def test_runSQL():
    table_name = 'norm_test'
    runsql_task = RunSQL(f'drop table {table_name}')
    runsql_task.run()

    dbm = DBmanager("sqlite_080323.db")
    connection = dbm.connect()
    select_query = f"SELECT * from {table_name}"
    cursor = connection.cursor()
    # fail if table exists
    with pytest.raises(sqlite3.OperationalError):
        cursor.execute(select_query)
        result = cursor.fetchall()
        print(result)
        cursor.close()
        connection.close()
    cursor.close()
    connection.close()
