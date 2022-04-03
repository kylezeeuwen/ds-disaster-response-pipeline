#!/bin/bash

USAGE="Usage: ./run.sh (generate|view) MODEL_NAME [SAMPLE_RATE]"

if [ $# -lt 2 ]
  then
    echo "ERROR: missing required params (generate|view) MODEL_NAME" 1>&2
    echo $USAGE 1>&2
    exit 1
fi

if [ $1 == 'view' ]; then
    GENERATE=0
    VIEW=1
elif [ $1 == 'generate' ]; then
    GENERATE=1
    VIEW=1
else
    echo "ERROR: $1 is invalid, it must be 'generate' or 'view'. Specify 'generate' to generate a model then view it in app, or 'view' to skip generate and view an existing model in app" 1>&2
    echo $USAGE 1>&2
    exit 1
fi
echo "MODE is $1"

MODEL_NAME=$2
echo "MODEL_NAME is $MODEL_NAME"

SAMPLE_RATE=1
if [ $# -eq 3 ]
  then
    SAMPLE_RATE=$3
fi
echo "SAMPLE_RATE is $SAMPLE_RATE"

MYSQL_ROOT_PASSWORD='not_secure1'
MYSQL_DATABASE='disaster_response'
MYSQL_USER='disaster_response'
MYSQL_PASSWORD='disaster_response'
MYSQL_HOST='mysql'

# NB `docker-compose run` and `docker-compose up` use different signatures to pass env vars so currently i have to generate two strings
# NB adding new ENV VARS: env vars specified here will pass direct to containers via `docker-compose run`, but for `docker-compose up` you must also add the env var to the service environment array in the docker-compose.yml file
# TODO consolidate these string generators to avoid duplication and future copy/paste errors
DOCKER_RUN_APP_ENV="-e MODEL_NAME=$MODEL_NAME -e SAMPLE_RATE=$SAMPLE_RATE -e MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD -e MYSQL_DATABASE=$MYSQL_DATABASE -e MYSQL_USER=$MYSQL_USER -e MYSQL_PASSWORD=$MYSQL_PASSWORD -e MYSQL_HOST=$MYSQL_HOST"
DOCKER_COMPOSE_ENV_PREPEND="SAMPLE_RATE=$SAMPLE_RATE MODEL_NAME=$MODEL_NAME MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD MYSQL_DATABASE=$MYSQL_DATABASE MYSQL_USER=$MYSQL_USER MYSQL_PASSWORD=$MYSQL_PASSWORD MYSQL_HOST=$MYSQL_HOST"

# TODO must merge docker and docker-compose setups can have both

set -x

docker-compose build process_data train_classifier flask_app 1>/dev/null 2>/dev/null

docker-compose up -d mysql 1>/dev/null 2>/dev/null

if [ $GENERATE -eq 1 ]
  then
    docker-compose run $DOCKER_RUN_APP_ENV process_data
    docker-compose run $DOCKER_RUN_APP_ENV train_classifier
fi

if [ $VIEW -eq 1 ]
  then
    command="$DOCKER_COMPOSE_ENV_PREPEND docker-compose --profile launch_app up -d"
    eval $command
fi

echo "open http://localhost:5000 in a browser"