FROM apache/airflow:2.8.4-python3.10

USER root

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    ca-certificates \
    && apt-get clean

USER airflow

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

