
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

## Run notebooks via docker

This repo assumes a local docker installation, and uses the jupyter/datascience-notebook to create a portable workspace that requires no other installation.

To get this running locally on OSX or Linux:
  * install [docker desktop](https://www.docker.com/products/docker-desktop)
  * in your terminal of choice with CWD set to the repo root execute: `./bin/go.sh`
  * in the lines of text output, find the localhost link and copy/paste it into your browser. Example link:
    * `http://127.0.0.1:8888/lab?token=abc123beepbeep456boopboop`

`./bin/go.sh` creates a docker container hosting the jupyter notebook with a mount the the `./notebooks` directory of this repo.

This is the content of the bin/go file circa Nov 20, 2021:

```js
docker run --rm -p 8888:8888 --name ds-drp -e JUPYTER_ENABLE_LAB=yes -v $(pwd)/notebook:/home/jovyan/work jupyter/datascience-notebook:latest
```

## Run pythong scripts

TODO

# Motivation

From above:

> The author is a noob data scientist completing the Udacity Data Science Nano degree, and the second assignment requires a repo.

TODO

# File Descriptors

TODO 

# How to interact with project

The `ipynb` files should not be read directly using an IDE - they are meant to be interacted with using a browser. The Installation section above outlines how to run `./bin/go.sh` and then copy/paste the provided URL into a browser.

All notebooks can be rerun to reproduce the results.

If you want to contribute, fork and submit a PR, that would be top notch.

# Licencing

Go nuts. Really, just get right in there.

[MIT License](./LICENSE)

# Authors

This is the work of Kyle Zeeuwen. There is lots of borrowed code from the Udacity course material. 

# Acknowledgements

* Udacity is so far so good 👍. TODO. Some summary notes can be found [here](./docs/project_rubric.md) 
* Figure Eight (TODO)[TODO] provided the pre classifier message data.