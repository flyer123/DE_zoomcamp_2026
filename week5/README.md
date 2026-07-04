# NYC Taxi Data Pipeline (DuckDB + Bruin + Docker)

## Overview

This project builds a Docker-based data pipeline that loads NYC taxi data into DuckDB using Bruin.  
All dependencies run inside a container — no local installation is required.

The pipeline performs:

- Data ingestion of NYC taxi trip data
- Data staging and transformation
- Report generation

---

## Project Architecture
Host Machine
↓
Docker Container (bruin-nyc)
↓
Bruin Pipeline
↓
DuckDB Storage


Everything runs inside Docker for reproducibility and isolation.

---

## Prerequisites

Make sure you have installed:

- Docker
- Docker Compose

Verify installation:

```bash
docker --version
docker compose version

Project Setup and Execution

Run the following commands in order.

Step 1 — Build Docker Image

  sudo docker compose build --no-cache

  Builds the container with all required dependencies.    

Step 2 — Start Container
  
  sudo docker compose up -d

  Starts the pipeline container in the background.

Step 3 — Enter Container
  
  sudo docker exec -it bruin-nyc bash

  You are now inside the container shell.

Running the Pipeline

  Run the following commands inside the container.

Step 4 — Run Report Asset
  
  bruin run reports.trips_report ./pipeline/pipeline.yml

  Executes the report generation asset.

Step 5 — Run Full Pipeline (Initial Load)

  bruin run ./pipeline/pipeline.yml \
  --start-date 2022-01-01 \
  --end-date 2022-02-01 \
  --full-refresh
  This command:

    Loads NYC taxi data

    Processes staging layer

    Creates tables from scratch

    Runs the pipeline for the specified date range

    --full-refresh ensures tables are created during the first run.

sudo docker compose down
  
  sudo docker compose down

Notes

    No local installation of pipeline dependencies is required.

    All processing happens inside Docker.

    DuckDB storage is managed by the container.