# mini-RAG

This is a minimal implementation of the RAG model for question answering.

## Requirements

- Python >= 3.8

## Install Dependencies (For Ubuntu)

```bash
sudo apt update
sudo apt install libpq-dev gcc python3-dev
```

## Installation

1. Download and install MiniConda from [here](https://docs.anaconda.com/miniconda/#quick-command-line-install)

2. Create a new conda environment with the following command:

```bash
conda create -n mini-rag python=3.10.12
```

3. Activate the environment:

```bash
conda activate mini-rag
```

4. Install the required packages:

```bash
cd src
pip install -r requirements.txt
```

(Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

5. Setup the environment variable:

```bash
cp .env.example .env
```

**Set your environment variables in the `.env` file.**

## Database Migrations

For details on database migrations using Alembic, please refer to the README file located at `/src/models/db_schemas/miniRAG`.

## Run the Docker container

```bash
cd ../docker
cp .env.example .env
```

**Update the `.env` file with your credentials.**

```bash
docker-compose up -d
```

## Run the FASTAPI server

```bash
cd ../src
uvicorn main:app --host '0.0.0.0' --port 5000 --reload
```

## POSTMAN Collection

You can download the POSTMAN collection for this project from `/src/assets/mini-RAG-app.postman_collection.json`.
