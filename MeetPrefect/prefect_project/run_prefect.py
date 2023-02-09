import random
import pandas as pd
from prefect import task, flow


# python3 run_prefect.py

@task
def load_data():
    data = pd.read_csv("prefect_project/DATA/original.csv")
    return data


@task
def add_column_with_random(data: pd.DataFrame):
    # df = pd.read_csv("../DATA/original.csv")
    data['random_number'] = random.randint(0, 100)
    data.to_csv("prefect_project/DATA/result_operation.csv")
    return data['random_number']


@task
def split_url(data: pd.DataFrame):
    # df = pd.read_csv("../DATA/original.csv")
    data['domain_of_url'] = data['url'].replace(to_replace='^https?:\/\/', value='', regex=True)
    data.to_csv("prefect_project/DATA/result_asset.csv")
    return data['domain_of_url']


@task
def merge_second_df(col1, col2):
    data = pd.DataFrame()
    data["col1"] = col1
    data["col2"] = col2
    data.to_csv("prefect_project/DATA/second.csv")


@flow
def meeting_prefect():
    df = load_data()
    column_with_random_nums = add_column_with_random(df)
    column_with_domain = split_url(df)
    merge_second_df(column_with_domain, column_with_random_nums)


def start():
    print(meeting_prefect())


# start()
