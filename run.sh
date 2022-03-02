#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "specify model name" 1>&2
    exit 1
fi

MODEL_NAME=$1
echo "MODEL_NAME is $MODEL_NAME"

MYSQL_ROOT_PASSWORD='not_secure1'
MYSQL_DATABASE='disaster_response'
MYSQL_USER='disaster_response'
MYSQL_PASSWORD='disaster_response'
MYSQL_HOST='mysql'

DOCKER_RUN_APP_ENV="-e MODEL_NAME=$MODEL_NAME -e MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD -e MYSQL_DATABASE=$MYSQL_DATABASE -e MYSQL_USER=$MYSQL_USER -e MYSQL_PASSWORD=$MYSQL_PASSWORD -e MYSQL_HOST=$MYSQL_HOST"
DOCKER_COMPOSE_ENV_PREPEND="MODEL_NAME=$MODEL_NAME MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD MYSQL_DATABASE=$MYSQL_DATABASE MYSQL_USER=$MYSQL_USER MYSQL_PASSWORD=$MYSQL_PASSWORD MYSQL_HOST=$MYSQL_HOST"

# TODO must merge docker and docker-compose setups can have both

# not currently needed
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

set -x

docker-compose build process_data train_classifier flask_app

docker-compose up -d mysql
docker-compose run $DOCKER_RUN_APP_ENV process_data
docker-compose run $DOCKER_RUN_APP_ENV train_classifier
command="$DOCKER_COMPOSE_ENV_PREPEND docker-compose --profile launch_app up -d"

eval $command

echo "open http://localhost:5000 in a browser"