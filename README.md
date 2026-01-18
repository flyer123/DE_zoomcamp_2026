# flyer123-flyer123-DE_zoomcamp_hw_1
# NYC Green Taxi Data Ingestion Pipeline

This repository contains a simple, reproducible data ingestion pipeline that downloads NYC **Green Taxi** trip data and **Taxi Zone lookup data**, loads them into Pandas, and writes them into a **PostgreSQL** database.

The project is designed as a learning-oriented pipeline aligned with Data Engineering and DevOps fundamentals (Docker, PostgreSQL, Pandas, SQLAlchemy).

---

## What This Pipeline Does

1. Downloads **Green Taxi trip data** (Parquet format) for a specified year and month  
2. Downloads **Taxi Zone lookup data** (CSV)  
3. Loads both datasets into Pandas  
4. Applies explicit schema casting (nullable integers, floats, strings, datetimes)  
5. Inserts the data into PostgreSQL as two tables:
   - `green_taxi_data`
   - `taxi_zone`

---

## Data Sources

- **Green Taxi Trips (Parquet)**  
  CloudFront CDN (NYC TLC official data):
https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_YYYY-MM.parquet

- **Taxi Zone Lookup (CSV)**  
DataTalksClub mirror:
https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv

---

## Tables Created

### `green_taxi_data`

Contains trip-level data, including:
- VendorID
- Pickup and dropoff timestamps (`lpep_pickup_datetime`, `lpep_dropoff_datetime`)
- Passenger count
- Trip distance
- Fare breakdown
- Location IDs
- Payment type

All nullable integer columns use Pandas `Int64` dtype to preserve NULLs.

---

### `taxi_zone`

Lookup table mapping `LocationID` to:
- Borough
- Zone
- Service zone

---

## Technology Stack

- Python 3.13
- Pandas
- Requests
- SQLAlchemy
- PostgreSQL 17
- Docker & Docker Compose
- pgAdmin

---

## Running with Docker Compose

### PostgreSQL & pgAdmin

```yaml
services:
db:
  image: postgres:17-alpine
  container_name: postgres
  environment:
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: postgres
    POSTGRES_DB: ny_taxi
  ports:
    - "5433:5432"
  volumes:
    - vol-pgdata:/var/lib/postgresql/data

pgadmin:
  image: dpage/pgadmin4
  container_name: pgadmin
  environment:
    PGADMIN_DEFAULT_EMAIL: pgadmin@pgadmin.com
    PGADMIN_DEFAULT_PASSWORD: pgadmin
  ports:
    - "8085:80"

volumes:
vol-pgdata:

Postgres is accessible:

From host: localhost:5433

From containers on the same network: host name postgres, port 5432

Running the Ingestion Script
Build the image: docker build -t python_image .

Run the ingestion:
docker run --network=container:postgres python_image \
  --pg-user postgres \
  --pg-pass postgres \
  --pg-host postgres \
  --pg-port 5432 \
  --pg-db ny_taxi \
  --year 2025 \
  --month 11

Important Implementation Notes:

    - Parquet files are downloaded manually using requests to avoid HTTP 403 issues.

     - pd.read_parquet() does not support dtype, so type casting is done after loading.

     - Datetime columns are explicitly converted using pd.to_datetime.

     - Column names are preserved exactly as in the source (e.g. VendorID with uppercase letters).

     - When running inside Docker, localhost does not refer to the host machine.



