Airflow + GCS Parquet Pipeline (Docker Compose)

This project runs Apache Airflow in Docker Compose and uses it to process Parquet files stored in Google Cloud Storage (GCS).

Prerequisites

Docker ≥ 20.x

Docker Compose v2

A Google Cloud project

A GCP service account key file (.json)

Ports 8080 available on localhost

Project Structure (relevant parts)
.
├── dags/
├── data/
│   └── raw/
├── gcp/
│   └── service_account.json   # ← your credentials
├── docker-compose.yml
└── README.md

1. Add Google Cloud credentials

Create a service account in GCP with at least:

Storage Object Viewer

BigQuery Data Editor (if loading into BQ)

Download the JSON key

Place it into the project:

gcp/service_account.json


⚠️ Do not commit this file to git.

2. Fix permissions for Airflow containers

Airflow containers run as user UID 50000.
Fix ownership and permissions on the data directory:

sudo chown -R 50000:0 data
sudo chmod -R 775 data


This is required to avoid PermissionError when tasks write files.

3. Build Docker images

Rebuild everything from scratch:

docker compose build --no-cache

4. Initialize Airflow database

Run the Airflow initialization container once:

docker compose up airflow-init


Wait until you see:

Database migrating done!

5. Start Airflow services

Start all Airflow components in detached mode:

docker compose up -d


This starts:

Webserver

Scheduler

Triggerer

Postgres (metadata DB)

6. Create Airflow admin user

Create a UI login user manually:

docker compose exec --user airflow airflow-webserver \
  airflow users create \
    --username airflow \
    --password airflow \
    --firstname Airflow \
    --lastname Admin \
    --role Admin \
    --email admin@example.com

7. Access Airflow UI

Open your browser:

http://localhost:8080


Login with:

Username: airflow

Password: airflow

Common Issues
DAGs not visible

Ensure DAG files are inside the dags/ directory

Check logs:

docker compose logs airflow-scheduler

Permission denied errors

Re-run:

sudo chown -R 50000:0 data
sudo chmod -R 775 data

Web UI not opening

Check container status:

docker compose ps

Notes

External tables read data directly from GCS

Native BigQuery tables store data inside BigQuery

Always use logical_date in DAGs for reproducible backfills
