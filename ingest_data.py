#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
import requests

# -------------------------
# Schema definitions
# -------------------------

dtype_taxi = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64",
    "ehail_fee": "float64",
    "trip_type": "string",
    "cbd_congestion_fee": "float64",
}

parse_dates = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime",
]

dtype_zone = {
    "LocationID": "Int64",
    "Borough": "string",
    "Zone": "string",
    "service_zone": "string",
}

DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0"}

# -------------------------
# CLI
# -------------------------

@click.command()
@click.option("--pg-user", default="postgres", help="PostgreSQL user")
@click.option("--pg-pass", default="postgres", help="PostgreSQL password")
@click.option("--pg-host", default="postgres", help="PostgreSQL host")
@click.option("--pg-port", default=5432, type=int, help="PostgreSQL port")
@click.option("--pg-db", default="ny_taxi", help="PostgreSQL database name")
@click.option("--year", default=2025, type=int, help="Year of the data")
@click.option("--month", default=11, type=int, help="Month of the data")
@click.option("--target-table-taxi", default="green_taxi_data")
@click.option("--target-table-zone", default="taxi_zone")
def run(
    pg_user,
    pg_pass,
    pg_host,
    pg_port,
    pg_db,
    year,
    month,
    target_table_taxi,
    target_table_zone,
):
    """Ingest NYC taxi data into PostgreSQL database."""
    year=2025
    month=11

    prefix = "https://d37ci6vzurychx.cloudfront.net/trip-data"
    taxi_url = f"{prefix}/green_tripdata_{year}-{month:02d}.parquet"
    # taxi_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet'
    zone_url = (
        "https://github.com/DataTalksClub/nyc-tlc-data/"
        "releases/download/misc/taxi_zone_lookup.csv"
    )
    
    # -------------------------
    # Download Parquet
    # -------------------------

    response = requests.get(taxi_url, headers=DEFAULT_HEADERS, timeout=30)
    response.raise_for_status()

    print(f"Downloading: {taxi_url}")

    parquet_file = "taxi.parquet"
    with open(parquet_file, "wb") as f:
        f.write(response.content)

    # -------------------------
    # Load data
    # -------------------------

    df_taxi = pd.read_parquet(parquet_file)

    # Cast types explicitly AFTER load
    for col, dtype in dtype_taxi.items():
        if col in df_taxi.columns:
            df_taxi[col] = df_taxi[col].astype(dtype)

    # Ensure datetime columns
    df_taxi[parse_dates] = df_taxi[parse_dates].apply(pd.to_datetime)
    
    # Cast types for date columns
    datetime_cols = [
        c for c in df_taxi.columns
        if "pickup" in c and "datetime" in c
        or "dropoff" in c and "datetime" in c
    ]

    df_taxi[datetime_cols] = df_taxi[datetime_cols].apply(pd.to_datetime)

    df_zone = pd.read_csv(
        zone_url,
        dtype=dtype_zone,
    )

    # -------------------------
    # Write to Postgres
    # -------------------------

    engine = create_engine(
        f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    )

    df_taxi.to_sql(
        name=target_table_taxi,
        con=engine,
        if_exists="replace",
        index=False,
    )

    df_zone.to_sql(
        name=target_table_zone,
        con=engine,
        if_exists="replace",
        index=False,
    )


if __name__ == "__main__":
    run()
