#!/bin/bash

# this script does the following:
# * Get parameters from command line
# * Build environment variable strings
# * start services and execute tasks

USAGE="Usage: ./run.sh (generate|view) MODEL_NAME [SAMPLE_RATE]"

######
# Get parameters from command line

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
echo "run.sh: MODE is $1"

MODEL_NAME=$2
echo "run.sh: MODEL_NAME is $MODEL_NAME"

SAMPLE_RATE=1
if [ $# -eq 3 ]
  then
    SAMPLE_RATE=$3
fi
echo "run.sh: SAMPLE_RATE is $SAMPLE_RATE"

######
# Build environment variable strings

MYSQL_ROOT_PASSWORD='not_secure1'
MYSQL_DATABASE='disaster_response'
MYSQL_USER='disaster_response'
MYSQL_PASSWORD='disaster_response'
MYSQL_HOST='mysql'

# NB `docker-compose run` and `docker-compose up` use different signatures to pass env so we have to generate two strings
# NB adding new ENV VARS: env vars specified here will pass direct to containers via `docker-compose run`, but for `docker-compose up` you must also add the env var to the service environment array in the docker-compose.yml file

DOCKER_COMPOSE_ENV_STRING="SAMPLE_RATE=$SAMPLE_RATE MODEL_NAME=$MODEL_NAME MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD MYSQL_DATABASE=$MYSQL_DATABASE MYSQL_USER=$MYSQL_USER MYSQL_PASSWORD=$MYSQL_PASSWORD MYSQL_HOST=$MYSQL_HOST"
DOCKER_RUN_APP_ENV_STRING=""
for env_var in $DOCKER_COMPOSE_ENV_STRING
do
  DOCKER_RUN_APP_ENV_STRING+="-e $env_var "
done

######
# start services and execute tasks

command="$DOCKER_COMPOSE_ENV_STRING docker-compose up -d mysql"
eval $command


if [ $GENERATE -eq 1 ]
  then
    echo "run.sh: building process_data container"
    docker-compose build process_data 1>/dev/null 2>/dev/null
    echo "run.sh: running process_data task"
    docker-compose run $DOCKER_RUN_APP_ENV_STRING process_data
    echo "run.sh: building train_classifier container"
    docker-compose build train_classifier 1>/dev/null 2>/dev/null
    echo "run.sh: running train_classifier task"
    docker-compose run $DOCKER_RUN_APP_ENV_STRING train_classifier
fi

if [ $VIEW -eq 1 ]
  then
    echo "run.sh: building build_react container"
    docker-compose build build_react 1>/dev/null 2>/dev/null
    echo "run.sh: running build_react task"
    docker-compose run build_react 1>/dev/null 2>/dev/null

    echo "run.sh: building flask_app container"
    docker-compose build flask_app
    echo "run.sh: running flask_app task"
    command="$DOCKER_COMPOSE_ENV_STRING docker-compose --profile flask_app up -d"
    eval $command
fi

echo "open http://localhost:5000 in a browser"
