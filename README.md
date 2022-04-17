# Disaster Response Message Classification Pipeline

## Overview

This code in this repo uses the Python [pandas](https://pandas.pydata.org/) , [nltk](https://www.nltk.org/), [scikit-learn](https://scikit-learn.org/) to build a model that classifies  messages sent during a disaster to assist agencies responding to the disaster.

The frontend is a [react](https://reactjs.org/) single page app built using the [create-react-app](https://reactjs.org/docs/create-a-new-react-app.html) tool. The front end makes requests to a python based [flask](https://flask.palletsprojects.com/en/2.1.x/) app that invokes the trained model to classify messages that are entered by the user. The frontend uses [Material UI](https://mui.com/) for its component library

The author is a noob data scientist completing the [Udacity Data Science Nano degree](https://www.udacity.com/course/data-scientist-nanodegree--nd025), and this is the submission for the second assignment in the course. The requirements and criteria are summarised in [this rubric file](./docs/project_rubric.md)

### Business Overview

Several assets were produced and made available in this repo:

* Data ETL Pipeline to format the training data for consumption by a ML classifier training pipeline : [process_data.py](./python-backend-src/tasks/process_data.py)
* Model building script to produce a trained ML classifier : [train_classifier.py](./python-backend-src/tasks/train_classifier.py)
* Webapp backend that serves data to the frontend : [flask_app.py](./python-backend-src/tasks/flask_app.py)
* Dashboard for interacting with classifier and understanding the data : [App.js](./react-frontend-src/src/App.js)

## Installation Notes

This repo relies heavily on docker to provide a completely portable deliverable. If you have docker installed and are in a OSX or Linux environment, there should be no other prerequisites. On Windows there may be some slight file system path issues, please send feedback to the maintainer if this is the case.

To get this running locally on OSX or Linux:
  * install [docker desktop](https://www.docker.com/products/docker-desktop)

## Local Execution

You can do a full execution or you can skip the training and use the trained classifier that comes with the repo. 

### Full execution including training

In terminal, with CWD set to the repo root, execute: `./run.sh generate DEFAULT_MODEL`

The command sequence above performs the following steps:
  * builds several docker containers
  * starts a MySQL instance in a docker container 
  * runs [process_data.py](./python-backend-src/tasks/process_data.py) : loads CSV files, transforms, and saves them to the local MySQL instance
  * runs [train_classifier.py](./python-backend-src/tasks/train_classifier.py) : builds a model, saves the model to the local filesystem and saves performance metrics to the local MySQL instance
  * builds the [react app](./react-frontend-src/src/App.js)
  * runs [flask_app.py](./python-backend-src/tasks/flask_app.py) : starts a local web server that can serve the react app, provide model metric, and classify messages

Once this is complete, you can view the web app at https://localhost:5000

### Skip training, use existing model

TODO: choose and commit a model
In terminal, with CWD set to the repo root, execute: `./run.sh view DEFAULT_MODEL`

The command sequence above performs the following steps:
  * builds several docker containers
  * starts a MySQL instance in a docker container 
  * runs [process_data.py](./python-backend-src/tasks/process_data.py) : loads CSV files, transforms, and saves them to the local MySQL instance
  * **the train_classifier IS NOT RUN in this mode**   
  * builds the [react app](./react-frontend-src)
  * runs [flask_app.py](./python-backend-src/tasks/flask_app.py) : starts a local web server that can serve the react app, provide model metric, and classify messages

Once this is complete, you can view the web app at https://localhost:5000

## Motivation

From above:

> The author is a noob data scientist completing the Udacity Data Science Nano degree, and this is the second assignment.

## Development Notes

### Run the react app in dev mode with live reload

Prerequisites: `nodejs 14 or greater`

Two steps performed on two terminals:

* `./run.sh view SOME_EXISTING_MODEL`: this gives you a running MySQL instance and a flask app running on port 5000 answering HTTP requests
* `cd react-frontend-src; npm install; npm start`: this runs the create-react-app dev tooling in live reload mode. Important: view the dev react on port localhost:3000, not port localhost:5000  

### Run a python script locally, not via docker

In many cases during development it is preferable to run the python directly instead of inside a docker container. For example:

* you are iterating and want shorter iteration times
* you want to debug with breakpoints and dont want to deal with the added complexity of docker
* you think it will be faster on bare metal

In any case all you need to do three things after first changing directory into `python-backend-src`:
  * setup a python virtual environment and install dependencies: `python3 -m venv venv; source ./venv/bin/activate; pip3 install -r requirements.txt`
  * set the same ENV that the `./run.sh` and `docker-compose.yml` file were providing. See the [env.py](python-backend-src/config/env.py) for a complete set of expected ENV vars. A set that works at the time of writing is provided in the examples below
  * ensure the MySQL instance is running (we still use docker for this): `(from repo root): docker-compose up -d mysql`  
  * run `ENV1=A ENV2=B python3 main.py (process_data|train_classifier|flask_app)`

Full example for `train_classifier` with all required ENV as at time of writing this README:

```
MODEL_NAME=CHANGE_MODEL_NAME SAMPLE_RATE=1 MYSQL_DATABASE=disaster_response MYSQL_USER=disaster_response MYSQL_PASSWORD=disaster_response MYSQL_HOST=localhost CSV_DIR=../docker-data/csv MODEL_DIRPATH=../docker-data/models python3 main.py train_classifier
```

### View flask_app logs

The `flask_app` is started using docker-compose in daemon mode (`-d`) so the logs are not printed to standard output. To see the server logs run either of these commands:

* `docker logs flask_app` : this will print all the logs and exit
* `docker logs -f flask_app` : this will print all the logs and continue printing logs as they are written

Note that if you want to see output it is best to call `print(FOO, flush=True)` in python to ensure logs are immediately flushed.

### Areas of Future Work
  * APP: quote from react output "The bundle size is significantly larger than recommended."
  * CODE QUALITY: metrics should be a class as I pass it around a lot
  * NLP STEPS: Better lemmetiser ?
  * NLP STEPS: Include POS (position of sentence) considerations when lemmatising
  * NLP STEPS: Apply Named Entity Recognition (NER)
  * NLP STEPS: Use Spanish not English
  * CLASSIFIER: do i do anything with genre ?
  * CLASSIFIER: train classifier - how is it being scored
  * CLASSIFIER: TODO allow selection of non latest MODEL-version overrides
  * CLASSIFIER: evaluate alternatives to demonstrate an "OR" in pipeline ?    
  * PRESENTATION: allow selection of specific categories in the UI
  * PRESENTATION: get samples of messages based on classification
  * EVALUATION: more evaluation metrics : precision score, f1 score, recall, and support scores.
    * compare accuracy between training and testing, it should be comparable otherwise there is overfitting
  * CLASSIFIER: evaluate solutions for comparing multiple classifiers via a pipeline, sounds like it is not suported out ogf box but there are some standard solutions
    * https://stackoverflow.com/questions/51629153/more-than-one-estimator-in-gridsearchcvsklearn/51629917#51629917
    * https://stackoverflow.com/questions/23045318/grid-search-over-multiple-classifiers

### Metabase Notes 

Although I opted to not use metabase in repo, these are the notes in case I add it back
 
  * connecting metabase to mysql
    * docker compose has a link that names mysql host as `mysql`
    * need to add `allowPublicKeyRetrieval=true` to connection settings options to workaround `RSA public key is not available client side (option serverRsaPublicKeyFile not set)` error  

  * metabase docker compose entry


    metabase:
      container_name: metabase
      image: 'metabase/metabase:v0.42.0'
      ports:
        - '3000:3000'
      volumes:
        - './docker-data/metabase-data:/metabase-data'
      links:
        - 'mysql:mysql'
      environment:
        MB_DB_FILE: /metabase-data/metabase.db

### How was the React App bootstrapped ?

It was extremely easy to add react to the repo

* followed instructions [here](https://reactjs.org/docs/create-a-new-react-app.html)


    npx create-react-app my-app
    cd my-app
    npm start 

* similarly MUI just worked out of the box. Followed instructions [here](https://mui.com/material-ui/getting-started/installation/)

## Licencing

Go nuts. Really, just get right in there.

[MIT License](./LICENSE)

## Authors

This is the work of Kyle Zeeuwen. There is lots of borrowed code from the Udacity course material. 

## Acknowledgements

* [Udacity](https://www.udacity.com/) is so far so good 👍. Some summary notes can be found [here](./docs/project_rubric.md) 
* Figure Eight - now known as Appen - https://appen.com/ - provided the pre classifier message data 🙏
