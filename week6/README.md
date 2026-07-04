# PySpark Docker Cluster – Quick Start Guide

## Project Overview

This project runs a small **Apache Spark cluster in Docker** with:

* Spark Master
* Spark Worker
* PySpark Jupyter Notebook

It allows you to test **distributed PySpark jobs** locally and explore datasets such as the **NYC Yellow Taxi dataset**.

---

# 1. Start the Environment

First ensure the data directory has permissions for the containers.

```bash
sudo chmod -R 777 ./data
```

Start the cluster:

```bash
sudo docker compose up -d
```

---

# 2. If the Containers Fail to Start

If something does not work (containers fail, notebook crashes, etc.), reset the environment:

```bash
sudo docker compose down -v
sudo docker rm -f pyspark-notebook 2>/dev/null
sudo docker compose up -d
```

---

# 3. Get the Jupyter Token

To access Jupyter, retrieve the authentication token:

```bash
sudo docker logs pyspark-notebook
```

Look for a line similar to:

```
http://127.0.0.1:8888/lab?token=XXXXXXXX
```

Copy the token.

---

# 4. Open the Interfaces

### Jupyter Notebook

Open in browser:

```
http://localhost:8888
```

Enter the token from the logs.

### Spark UI

```
http://localhost:8080
```

This UI shows:

* Running jobs
* Executors
* Workers
* Resource usage

---

# 5. Test the Spark Cluster

Create a new notebook and run:

```python
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("cluster-test")
    .master("spark://spark-master:7077")
    .config("spark.driver.host", "pyspark-notebook")
    .getOrCreate()
)

df = spark.range(10)
df.show()
```

If everything is configured correctly, Spark will execute the job and show numbers **0–9**.

---

# 6. Download a Dataset

Inside the notebook:

```python
!wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet -P /data
```

This downloads the **NYC Yellow Taxi dataset**.

---

# 7. Load the Dataset in Spark

Create a Spark session and read the parquet file:

```python
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("yellow taxi dataframe")
    .master("spark://spark-master:7077")
    .config("spark.driver.host", "pyspark-notebook")
    .getOrCreate()
)

df = spark.read.parquet("/data/yellow_tripdata_2025-11.parquet")

df.printSchema()
df.show(5)
```

This will:

1. Connect to the Spark cluster
2. Load the taxi dataset
3. Print the dataset schema
4. Show the first 5 rows

---

# 8. Useful Docker Commands

Check running containers:

```bash
sudo docker ps
```

View logs:

```bash
sudo docker logs pyspark-notebook
```

Stop the cluster:

```bash
sudo docker compose down
```

Reset everything:

```bash
sudo docker compose down -v
```

---

# 9. Expected Running Containers

After successful startup you should see:

```
spark-master
spark-worker
pyspark-notebook
```

---

# 10. Architecture

```
Jupyter Notebook
        │
        │ Spark Driver
        ▼
Spark Master (7077)
        │
        ▼
Spark Worker
        │
        ▼
Execute Spark Jobs
```

---

# End

This environment provides a simple local **Spark cluster for PySpark experimentation and data engineering practice**.
