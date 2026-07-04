# flyer123-flyer123-DE_zoomcamp_hw_2
This is a repository for Data Engineering Zoomcamp cohort 2026 homework 2


# what to do
run docker-compose.
execute 01-gcp-kv.yaml, add your creds manually, it will create key value pairs used in gcp object creation
execute02-gcp_setup.yaml - it will create bucket and BigQuery dataset
execute 04-gcp_taxi_scheduled for:
1 - 2021-01-01 -> 2012-07-31 for both yellow and green
2 - 2020-10-10 -> 2020-12-31 bor both yellow and green
it will download the csv files, and create tables in BigQuery