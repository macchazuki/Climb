# Climb

## Initial setup

Launch a postgres docker container and create a test db

```shell
# Bash
docker run -d --name climb_db \
-e POSTGRES_PASSWORD="greentea" \
-e POSTGRES_USER="maccha" \
-e POSTGRES_DB="climbdb" \
-p 5432:5432 postgres

# Windows
docker run -d --name climb_db ^
-e POSTGRES_PASSWORD="greentea" ^
-e POSTGRES_USER="maccha" ^
-e POSTGRES_DB="climbdb" ^
-p 5432:5432 postgres


docker exec -it climb_db bash

psql -h localhost -U maccha climbdb
climbdb=# create database climbdb_test;
```

Create virtualenv

```shell
virtualenv venv --python=python3.8

# For MacOS and Linux
source update_environment.sh
pip install -r requirements.txt

# For Windows
chmod +x update_environment.sh
source update_environment.sh
pip install -r requirements.txt
```

Run everytime you start a new terminal on this project

```shell
# from project root
source update_environment.sh
```

## Run Docker

```
docker build -t myimage .
docker run -d --name mycontainer -p 80:80 myimage
```

## Run Local

```shell
# from root directory
uvicorn src.main:app --reload
```

## Run migrations

Only run the following once you have `climbdb` running

```shell
# to create a new migration
alembic revision --autogenerate -m <commit message>

# to update to head
alembic upgrade head
```

## Testing

```shell
pytest -vv <your_test_file>

# Run all tests (recommended)
pytest -vv
```