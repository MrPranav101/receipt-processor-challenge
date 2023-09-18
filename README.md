# Receipt Processor

This is my submission to the fetch-rewards coding challenge. The goal of this project is to create a RESTful API that can
ingest a receipt and calculate points associated to the receipt.

## How to run

Considering that docker is installed your machine `docker compose up --build` from the root directory should be the easiest way to run the project.

If you can navigate to
[localhost:8080/docs](localhost:8080/docs). You should see the swagger documentation for the API.

## Implementation

I chose to implement this project using Python, FastAPI and sqlite. 

FastAPI because it is a very fast and easy to use for creating RESTful APIs. And it comes with automatic swagger generation :)

sqlite because it is a very simple database that is easy to use and does not require any setup.

The project is split into 3 main parts:
1. The database
   - I use sqlalchemy to create the database and the tables.
2. The API
3. The business logic/ Service Layer

## Testing
I am using pytest for testing. To run the tests run `python -m pytest` in the root directory of the project (given you have python and the dependencies installed).


## Logging
I am using the python logging library to log errors and warnings. The logs are output to stdout and stderr.
I also add an x-request-id to the logs so that it is easier to track a request through the logs.
