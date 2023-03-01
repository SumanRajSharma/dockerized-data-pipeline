# Dockerized Data Pipeline
This is a collection of scripts and Docker configuration files that enable the user to create a data pipeline for ingesting NY taxi data into a PostgreSQL database.

## Setup
To get started, you'll need to have Docker installed on your machine. Then, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the root of the repository.
3. Run the following command to start the Docker containers:

```bash
 docker-compose up 
```

This will start two containers: one for the PostgreSQL database and one for pgAdmin.

## PostgreSQL
The PostgreSQL container is pre-configured with a user and password, and a database called ny_taxi. The container also exposes port 5432, so you can connect to it using a tool like pgcli or any PostgreSQL client of your choice.

## pgAdmin
The pgAdmin container is pre-configured with a default email and password. Once the container is up and running, you can access the pgAdmin web interface by navigating to localhost:8080 in your web browser. From there, you can connect to the PostgreSQL database and manage it using the pgAdmin UI.

## Ingesting Data
Once the Docker containers are up and running, you can use the included Python script to ingest NY taxi data into the PostgreSQL database. Here's how:

1. Open a new terminal window.
2. Navigate to the root of the repository.
3. Run the following command to start the ingestion script:
```bash
docker-compose run ingest-data <arguments>
```
Replace `<arguments>` with the appropriate values for the following arguments:

- `--user`: the user name for PostgreSQL.
- `--password`: the password for PostgreSQL.
- `--host`: the host for PostgreSQL.
- `--port`: the port for PostgreSQL.
- `--db`: the database name for PostgreSQL.
- `--table_name`: the name of the table where we will write the results to.
- `--url`: the URL of the CSV file containing the NY taxi data.
For example:

```bash
docker-compose run ingest-data --user=root --password=root --host=pgdatabase --port=5432 --db=ny_taxi --table_name=taxi_trips --url=https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2019-01.csv
```
This will download the specified CSV file, transform it, and load it into the PostgreSQL database. The ingestion script uses pandas and sqlalchemy to handle the data and database operations.

## Requirements
The following dependencies are required to run the ingestion script:

- pandas==1.5.3
- psycopg2-binary==2.9.5
- sqlalchemy==2.0.4

## License
This project is licensed under the MIT License - see the LICENSE file for details.