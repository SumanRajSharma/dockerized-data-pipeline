# Dockerized Data Pipeline using [Prefect](https://docs.prefect.io/)
This repository contains the code for an ETL (extract, transform, load) pipeline that ingests and processes New York City taxi trip data from DataTalksClub/nyc-tlc-data, and loads the resulting data into a PostgreSQL database.

The pipeline is built using Python, Docker, and Prefect. The data is extracted from the source URL using wget, and then processed using pandas and SQLalchemy. The final processed data is loaded into a PostgreSQL database using the Prefect-SQLAlchemy integration.

## Project Structure
The project directory contains the following files and directories:

- Dockerfile: Specifies the Docker image to use for the pipeline.
- docker-compose.yml: Specifies the Docker containers to use for the pipeline, including PostgreSQL and pgAdmin.
- requirements.txt: Specifies the Python dependencies for the pipeline.
- ingest_data.py: Contains the code for the ETL pipeline.
- terraform/: Contains the Terraform code to deploy the infrastructure required to run the pipeline. (Not nedded for now)
- ny_taxi_postgres_data/: Contains the PostgreSQL data directory for persistent storage of the database.

## Getting Started
To get started with the pipeline, follow these steps:

1. Clone the repository to your local machine.
2. Install Docker and Docker Compose.
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
 docker build -t python:v0.0.1 .
 docker run --network pg-database-network python:v0.0.1
 ```

This will download the specified CSV file, transform it, and load it into the PostgreSQL database. The ingestion script uses pandas and prefect-sqlalchemy to handle the data and database operations.

## Note 
The db credentials are added to Prefect block using `SQLAlchemy Connector`. You need to configure this after running `docker build -t python:v0.0.1 .`
1. Access bash of the python container built
  ```
  docker exec -it <container_name> /bin/bash
  ```
2. Access Prefect orion API
  ```
  prefect orion start
  ```
3. Access Prefect dashboard at http://127.0.0.1:4200 
4. Select `Blocks` from side menu
5. Add new blocks button and select `SQLAlchemy Connector`; for reference see the screenshot
   <img width="1403" alt="Screenshot 2023-03-08 at 6 39 28 pm" src="https://user-images.githubusercontent.com/6215331/223654682-b9c3d9ee-0e2a-4a97-b379-cf7b46486cb5.png">
6. After creating the block you can access using this line (ingest_data.py)

  ```
  database_block = SqlAlchemyConnector.load("localhost-postgres-connector")
  with database_block.get_connection(begin=False) as engine:
  ```

## Requirements
The following dependencies are required to run the ingestion script:

- pandas==1.5.3
- psycopg2-binary==2.9.5
- sqlalchemy==1.4.46
- prefect==2.8.4
- prefect-sqlalchemy==0.2.4
- prefect-gcp[cloud_storage]==0.3.0
- protobuf==4.22.1
- pyarrow==11.0.0
- pandas-gbq==0.19.1

## License
This project is licensed under the MIT License - see the LICENSE file for details.
