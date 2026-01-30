from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

import os
import requests
from airflow.providers.google.cloud.hooks.gcs import GCSHook

# ---------------- CONFIG ----------------

month=6
year=2024

PARQUET_URL = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet"

LOCAL_PATH = f"/opt/airflow/data/raw/yellow_tripdata_{year}-{month:02d}.parquet"

GCS_BUCKET = "your-bucket-name"
GCS_OBJECT = f"yellow_tripdata_{year}-{month:02d}.parquet"

# ---------------- TASKS ----------------

def download_parquet():
    os.makedirs(os.path.dirname(LOCAL_PATH), exist_ok=True)

    with requests.get(PARQUET_URL, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(LOCAL_PATH, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)


def upload_to_gcs():
    hook = GCSHook()
    hook.upload(
        bucket_name=GCS_BUCKET,
        object_name=GCS_OBJECT,
        filename=LOCAL_PATH,
        mime_type="application/octet-stream",
    )

# ---------------- DAG ----------------

with DAG(
    dag_id="download_parquet_and_upload_to_gcs",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=["parquet", "gcs"],
) as dag:

    download = PythonOperator(
        task_id="download_parquet",
        python_callable=download_parquet,
    )

    upload = PythonOperator(
        task_id="upload_to_gcs",
        python_callable=upload_to_gcs,
    )

    download >> upload

