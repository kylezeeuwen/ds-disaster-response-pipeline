# Disaster Response Message Classification Pipeline

## Overview

This code in this repo uses the Python [pandas](https://pandas.pydata.org/) , [nltk](https://www.nltk.org/), [scikit-learn](https://scikit-learn.org/) to build a model that classifies  messages sent during a disaster to assist agencies responding to the disaster.

The frontend is a [react](https://reactjs.org/) single page app built using the [create-react-app](https://reactjs.org/docs/create-a-new-react-app.html) tool. The front end makes requests to a python based [flask](https://flask.palletsprojects.com/en/2.1.x/) app that invokes the trained model to classify messages that are entered by the user. The frontend uses [Material UI](https://mui.com/) for its component library

The author is a noob data scientist completing the [Udacity Data Science Nano degree](https://www.udacity.com/course/data-scientist-nanodegree--nd025), and this is the submission for the second assignment in the course. The requirements and criteria are summarised in [this rubric file](./docs/project_rubric.md)

## On Branches and versions of this repo

The current `main` and `submission` branch are a restructured and "undockerised" version of the repo. This is done to satisfy feedback on initial submissions.

The original "complete" dockerised version that includes the steps to transpile the react code into a bundle can be found in the `develop` branch.

### Business Overview

Several assets were produced and made available in this repo:

* Data ETL Pipeline to format the training data for consumption by a ML classifier training pipeline : [process_data.py](./workspace/process_data.py)
* Model building script to produce a trained ML classifier : [train_classifier.py](./workspace/train_classifier.py)
* Webapp backend that serves data to the frontend : [flask_app.py](./workspace/flask_app.py)
* Dashboard for interacting with classifier and understanding the data : [src App.js](./workspace/app/src/App.js)
  * REVIEWERS: [Here are the plotly visualisations](./workspace/app/src/ModelPerformance.js) 

## Running in the Udacity workspace

* `cd workspace`
* `python3 process_data.py`
* `python3 train_classifier.py`
* `python3 flask_app.py`

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

## Licencing

Go nuts. Really, just get right in there.

[MIT License](./LICENSE)

## Authors

This is the work of Kyle Zeeuwen. There is lots of borrowed code from the Udacity course material. 

## Acknowledgements

* [Udacity](https://www.udacity.com/) is so far so good 👍. I am slightly disheartened that I was required to undockerise my repo. Waiting to see how round 3 of feedback turns out. Some summary notes on assignment requirements can be found [here](./docs/project_rubric.md) 
* Figure Eight - now known as Appen - https://appen.com/ - provided the pre classifier message data 🙏
