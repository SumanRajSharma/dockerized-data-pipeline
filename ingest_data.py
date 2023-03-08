import os
import pandas as pd
from sqlalchemy import create_engine
from time import time
from datetime import timedelta
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_sqlalchemy import SqlAlchemyConnector


@task(log_prints=True, retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data(url):
    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    os.system(f"wget {url} -O {csv_name}")
    df = pd.read_csv(csv_name)
    return df
@task(log_prints=True, retries=3)
def transform_data(df):
    # changing the datatype of tpep_pickup_datetime and tpep_dropoff_datetime to pandas datetype
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    #removing the 0 passenger_count row from the dataframe
    print(f"pre: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    df =df[df['passenger_count'] != 0]
    print(f"post: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    return df

@task(log_prints=True, retries=3)
def load_data(table_name, df):
    database_block = SqlAlchemyConnector.load("localhost-postgres-connector")
    # Set the chunksize
    chunksize = 100000
    with database_block.get_connection(begin=False) as engine:
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
        for i in range(0, len(df), chunksize):
            try:
                chunk = df.iloc[i:i+chunksize]
                t_start = time()
                chunk.to_sql(name=table_name, con=engine, if_exists='append')
                t_end = time()
                print('inserted another chunk, took %.3f second' % (t_end - t_start))
            except StopIteration:
                print("Finished ingesting data into the postgres database")
                break


@flow(name="ingest Flow")
def main_flow(table_name: str):
    url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

    raw_data = extract_data(url)
    data = transform_data(raw_data)
    load_data(table_name, data)

if __name__ == '__main__':
    main_flow('yellow_taxi_trips')