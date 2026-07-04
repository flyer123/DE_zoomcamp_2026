"""@bruin
name: ingestion.trips
type: python
image: python:3.11

materialization:
  type: table
  strategy: append

connection: duckdb-default

columns:
  - name: pickup_datetime
    type: timestamp
    description: "When the meter was engaged"
  - name: dropoff_datetime
    type: timestamp
    description: "When the meter was disengaged"
@bruin"""

import os
import json
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"


def generate_month_list(start_date: str, end_date: str):
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)

    current = start.replace(day=1)
    months = []

    while current < end:
        months.append((current.year, current.month))
        current += relativedelta(months=1)

    return months


def normalize_columns(df: pd.DataFrame, taxi_type: str):
    """
    Normalizes yellow and green schemas into a common format.
    """

    column_mapping = {
        # yellow
        "tpep_pickup_datetime": "pickup_datetime",
        "tpep_dropoff_datetime": "dropoff_datetime",
        # green
        "lpep_pickup_datetime": "pickup_datetime",
        "lpep_dropoff_datetime": "dropoff_datetime",
    }

    df = df.rename(columns=column_mapping)

    required_columns = [
        "pickup_datetime",
        "dropoff_datetime",
        "PULocationID",
        "DOLocationID",
        "fare_amount",
        "payment_type",
    ]

    df = df[required_columns].copy()

    df = df.rename(columns={
        "PULocationID": "pickup_location_id",
        "DOLocationID": "dropoff_location_id",
    })

    df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
    df["dropoff_datetime"] = pd.to_datetime(df["dropoff_datetime"])

    df["taxi_type"] = taxi_type

    return df


def materialize():
    start_date = os.environ["BRUIN_START_DATE"]
    end_date = os.environ["BRUIN_END_DATE"]
    taxi_types = json.loads(os.environ["BRUIN_VARS"]).get("taxi_types", ["yellow"])

    months = generate_month_list(start_date, end_date)

    dataframes = []

    for taxi_type in taxi_types:
        for year, month in months:
            month_str = str(month).zfill(2)
            file_url = f"{BASE_URL}/{taxi_type}_tripdata_{year}-{month_str}.parquet"

            try:
                df = pd.read_parquet(file_url)
                df = normalize_columns(df, taxi_type)
                dataframes.append(df)
                print(f"Loaded {file_url}")
            except Exception as e:
                print(f"Skipping {file_url}: {e}")

    if not dataframes:
        return pd.DataFrame()

    final_dataframe = pd.concat(dataframes, ignore_index=True)

    return final_dataframe