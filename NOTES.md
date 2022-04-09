YOU ARE HERE / TODO:

  * remove all sqllite references
  
  * train calssifier - how is it being scored

  * High level remaining:
    * clean up CSS
    * fix dockerfile python + npm issue
    * python format and add docs
    * maybe add a test or two  
    
  * react strip out model name context - no longer needed
  * delete run_model_on_all_data

  * stretch : get samples of messages based on classification

  * reconcile flask_app vs launch_app naming

  * reconcile docker-data vs src/data

  * TODO allow MODEL-version overrides
  
  * re-enable some parameters

  * categories vs classifications

Milestones

  * (DONE) writing category, result, classifications, result_summary into database. The flask app is using the model to return results
  * (DONE) have working model, no idea if it works well 
  * (DONE) process data is done, need to start train_classifier. first step will be NLP to extract features.
  * (DONE) need to review material to extract examples into example project

Model Variations/Improvements
---

  * (DONE) FIXED by removing stopwords from the pickle file. I had to remove my tokenizer on a pickling/job dispatch error
  * Need to clean data in terms of empty colums first, or did I do that in process_data
  * Use Spanish not English
  * Include POS (position of sentence) considerations when lemmatising
  * Apply Named Entity Recognition (NER)
  * Better lemmetiser

# Metabase Notes 

* metabase admin
  * user: kyle_zeeuwen@gmail.com
  * password: not_secure1

* connecting metabase to mysql
  * docker compose has a link that names mysql host as `mysql`
  * need to add `allowPublicKeyRetrieval=true` to connection settings options to workaround `RSA public key is not available client side (option serverRsaPublicKeyFile not set)` error  


V1 App
  * use what they have provided
  * get basic metrics on performance of model and list the model characteristics


V2 App

  * Highly interative and react based
  * uses standard JSON data retrieval and client side rendering

Create React App Experiment
---

* following instructions here : https://reactjs.org/docs/create-a-new-react-app.html


    npx create-react-app my-app
    cd my-app
    npm start 

* so far works well
* TODO
  * npm run-scripts build needs to be part of build step for flask app
  * verify and document the dev pointing at built setup
* pause back to main, build up model tracking in DB and in lib    