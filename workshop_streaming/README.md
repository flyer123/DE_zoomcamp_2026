# Fully Dockerized Environment for Module 7 – Streaming

**Data Engineering Zoomcamp (Cohort 2026)**

This repository provides a **fully containerized setup** for the streaming workshop from **Module 7** of the Data Engineering Zoomcamp. The goal is to run the entire environment inside Docker so that no components need to be installed locally.

The setup follows the official workshop content:
https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/07-streaming/workshop

All services — including **Redpanda** and **Jupyter Notebook** — run in containers and communicate through the Docker network.

---

## Prerequisites

Before starting, ensure the following are installed on your system:

* **Docker**
* **Docker Compose**

---

## Build the Environment

Build the containers without using cached layers:

```
sudo docker compose build --no-cache
```

This guarantees that all dependencies are installed from scratch.

---

## Start the Services

Run the environment in detached mode:

```
sudo docker compose up -d
```

This command starts all required services, including the streaming broker and the Jupyter environment used for executing the workshop code.

---

## Access the Jupyter Environment

All workshop commands should be executed inside the **Jupyter container** rather than on the local machine.

To obtain the access URL and authentication token, run:

```
sudo docker compose logs jupyter
```

The output will include a URL similar to:

```
http://127.0.0.1:8888/?token=...
```

Open this URL in your browser to access the notebook environment.

---

## Running the Workshop

Once the environment is running:

* Open the notebook in Jupyter.
* Execute the same code and commands described in the official workshop materials.

Aside from running the code inside the containerized notebook environment, **the workflow remains identical to the original workshop instructions**.

---

## Workshop Video

The original workshop recording is available here:

https://www.youtube.com/watch?v=YDUgFeHQzJU

---

## Summary

This setup provides a reproducible environment where:

* All components run in Docker containers.
* No local Python environment is required.
* The workshop workflow remains unchanged.

It ensures consistent results across different machines and simplifies the setup process for the streaming module.


