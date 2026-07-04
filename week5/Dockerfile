FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Bruin CLI (official binary)
RUN curl -LsSf https://getbruin.com/install/cli | bash

RUN apt-get update && apt-get install -y git curl unzip ca-certificates

CMD ["bash"]