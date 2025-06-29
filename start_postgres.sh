#!/bin/bash

# Name of the Docker container
db_container="mixserver-postgres"

# Check if the container is already running
if [ "$(docker ps -q -f name=$db_container)" ]; then
  echo "Postgres container '$db_container' is already running."
  exit 0
fi

# If not running, check if it exists (stopped)
if [ "$(docker ps -aq -f name=$db_container)" ]; then
  echo "Starting existing Postgres container '$db_container'..."
  docker start $db_container
else
  echo "Creating and starting new Postgres container '$db_container'..."
  docker run --name $db_container -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -p 5432:5432 -d postgres:15
fi

echo "Postgres is ready on port 5432."
