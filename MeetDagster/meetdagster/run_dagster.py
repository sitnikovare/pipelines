import random
import pandas as pd
from dagster import op, job, asset

@op
def add_column_with_random():
    data = pd.read_csv("../DATA/original.csv")
    data['random_number'] = random.randint(0, 100)
    data.to_csv("../DATA/result_operation.csv")
    return data


@asset
def split_url():
    data = pd.read_csv("../DATA/original.csv")
    data['domain_of_url'] = data['url'].replace(to_replace='^https?:\/\/', value='', regex=True)
    data.to_csv("../DATA/result_asset.csv")
    return data


@job
def meeting_dagster():
    split_url()
    add_column_with_random()
