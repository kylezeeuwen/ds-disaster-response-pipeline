
# Overview

This code in this repo uses the Python [pandas](https://pandas.pydata.org/) , some NLP, and some ML (TODO references) to build a classifier for messages sent during a disaster.

The author is a noob data scientist completing the [Udacity Data Science Nano degree](https://www.udacity.com/course/data-scientist-nanodegree--nd025), and the second assignment requires:

* [a repo](https://github.com/kylezeeuwen/ds-disaster-response-pipeline/)

## Business Overview

Several assets were produced and made available in this repo:

* Data ETL Pipeline for format the training data for classifier generation
* Model building script to produce a trained ML classifier
* Dashboard for interacting with classifier and understanding the data

# Installation Notes

This repo assumes a local docker installation, and uses `docker-compose` to execute the data processing, model training, and app hosting. Using docker means that this workspace does not require any other installation.

To get this running locally on OSX or Linux:
  * install [docker desktop](https://www.docker.com/products/docker-desktop)
  * in your terminal of choice with CWD set to the repo root execute: `./run.sh MODEL_NAME`

`./run.sh` does the following things: TODO fill in once stable.

# Motivation

From above:

> The author is a noob data scientist completing the Udacity Data Science Nano degree, and the second assignment requires a repo.

TODO

# File Descriptors

TODO 

# How to interact with project

Depends if you want to gerenate a model or just use an existing model.

* If you want to generate a model then look at the results using the app: run `./run.sh generate MODEL_NAME` then open http://localhost:5000 in a browser
  * you can change MODEL_NAME to whatever you want
  
* If you want to skip model generation generate a model then look at the results using the app: just run `./run.sh view MODEL_NAME` then open http://localhost:5000 in a browser
  * model_name must be an existing model that is saved as `MODEL_NAME-latest.pkl` in the [./docker-data/models](./docker-data/models) directory

# Licencing

Go nuts. Really, just get right in there.

[MIT License](./LICENSE)

# Authors

This is the work of Kyle Zeeuwen. There is lots of borrowed code from the Udacity course material. 

# Acknowledgements

* Udacity is so far so good 👍. TODO. Some summary notes can be found [here](./docs/project_rubric.md) 
* Figure Eight (TODO)[TODO] provided the pre classifier message data.