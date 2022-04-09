new directory layout
docker-data
docs
python-backend-src
  Dockerfile
react-frontend-src
  Dockerfile
run.sh

YOU ARE HERE / TODO:
  * fix dockerfile python + npm issue
  * some apt-get install in dockerfile look unnecessary
  * react strip out model name context - no longer needed
  * improve model info presentation
  * reconcile flask_app vs launch_app naming
  * reconcile docker-data vs src/data
  * re-enable some parameters
  * categories vs classifications
  * CLASSIFIER: evaluate alternatives to demonetrate an "OR" in pipeline ?

DEFER
  * APP: The bundle size is significantly larger than recommended.
  * CODE QUALITY: metrics should be a class as I pass it around a lot
  * NLP STEPS: Better lemmetiser ?
  * NLP STEPS: Include POS (position of sentence) considerations when lemmatising
  * NLP STEPS: Apply Named Entity Recognition (NER)
  * CLASSIFIER: do i do anything with genre ?
  * CLASSIFIER: train classifier - how is it being scored
  * CLASSIFIER: TODO allow selection of non latest MODEL-version overrides
  * PRESENTATION: allow selection of specific categories in the UI
  * PRESENTATION: get samples of messages based on classification

WILL NOT DO
  * NLP STEPS: Use Spanish not English

Milestones
  * (DONE) writing category, result, classifications, result_summary into database. The flask app is using the model to return results
  * (DONE) have working model, no idea if it works well 
  * (DONE) process data is done, need to start train_classifier. first step will be NLP to extract features.
  * (DONE) need to review material to extract examples into example project

# Metabase Notes 

  * opted to not use metabase in repo, but these are the notes in case I add it back

  * metabase admin
    * user: kyle_zeeuwen@gmail.com
    * password: not_secure1
  
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

How was the React App bootstrapped ?
---

In general it was extremely easy to add react to the repo

- followed instructions [here](https://reactjs.org/docs/create-a-new-react-app.html)


    npx create-react-app my-app
    cd my-app
    npm start 

- similarly MUI just worked out of the box. Followed instructions [here](https://mui.com/material-ui/getting-started/installation/)