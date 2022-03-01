#!/bin/bash

MYSQL_DATABASE='disaster_response'
MYSQL_USER='disaster_response'
MYSQL_PASSWORD='disaster_response'
MYSQL_HOST='127.0.0.1'

# TODO must merge docker and docker-compose setups can have both

# not currently needed
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

docker-compose build process_data train_classifier flask_app
docker-compose up -d mysql
docker-compose run process_data
docker-compose run train_classifier
docker-compose --profile launch_app up -d

echo "open http://localhost:5000 in a browser"