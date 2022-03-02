YOU ARE HERE:
  * testing app changes via `drma; docker-compose build flask_app; docker-compose up -d mysql flask_app;  docker logs -f flask_app`
    * (DONE - could be improved) getting caught on container not rebuilding, causing stale code to run and changes to not take affect
    * `./run.sh takes care of this`
  
  * how to prevent repeated nltk downloads - slowing down iteration time  

  * how to add an init section to a flask app
  
  * model retrieval should be abstracted
    * can i get checksum of model factory file ?
  
  * reconcile flask_app vs launch_app naming

* build tooling to evaluate model
    * the UI of the app to show if its good
    * docker-compose of the steps, and maybe mysql + metabase
  * DONE: docker compose working, mysql working, 
  * DONE: write results into DB
    * need to make a data frame out of the messages with predicted and actual for each category

  * TODO: refactor to flat bin → lib structure
    extract sql_conn and tokenizer

  * TODO: save the model time, name, parameters into the pickle, and build downstream so we can select which model to use to classify

  * TODO: refactor results in DB so that we can save multiple models and compare

  * TODO: add visualisations and submit

  * TODO must merge docker and docker-compose setups can have both

Milestone (DONE)
  * writing category, result, classifications, result_summary into database. The flask app is using the model to return results

Milestone (DONE)
  * have working model, no idea if it works well 

Milestone (DONE)
  * process data is done, need to start train_classifier. first step will be NLP to extract features.
    * (DONE) need to review material to extract examples into example project

Potential Variations/Improvements
---
* FIXED by removing stopwords from the pickle file. I had to remove my tokenizer on a pickling/job dispatch error
* Need to clean data in terms of empty colums first, or did I do that in process_data
* Use Spanish not English
* Include POS (position of sentence) considerations when lemmatising
* Apply Named Entity Recognition (NER)
* Better lemmetiser

# Data Structure ETL to write to SQL

## X
Type pandas.core.series.Series
shape: (2618,)

## Y_actual
Type pandas.core.frame.DataFrame
shape: (2618, 36)

## Y_predicted
Type numpy.ndarray
shape: (2618, 36)

## (Pdb) Y_actual.columns
```
Index(['related', 'request', 'offer', 'aid_related', 'medical_help',
       'medical_products', 'search_and_rescue', 'security', 'military',
       'child_alone', 'water', 'food', 'shelter', 'clothing', 'money',
       'missing_people', 'refugees', 'death', 'other_aid',
       'infrastructure_related', 'transport', 'buildings', 'electricity',
       'tools', 'hospitals', 'shops', 'aid_centers', 'other_infrastructure',
       'weather_related', 'floods', 'storm', 'fire', 'earthquake', 'cold',
       'other_weather', 'direct_report'],
      dtype='object')

```

## Y_predicted post ETL columns
```
predicted_df = pd.DataFrame(Y_predicted)
predicted_df = predicted_df.set_axis(category_names, axis=1, inplace=False)

(Pdb) predicted_df.columns
Index(['related', 'request', 'offer', 'aid_related', 'medical_help',
       'medical_products', 'search_and_rescue', 'security', 'military',
       'child_alone', 'water', 'food', 'shelter', 'clothing', 'money',
       'missing_people', 'refugees', 'death', 'other_aid',
       'infrastructure_related', 'transport', 'buildings', 'electricity',
       'tools', 'hospitals', 'shops', 'aid_centers', 'other_infrastructure',
       'weather_related', 'floods', 'storm', 'fire', 'earthquake', 'cold',
       'other_weather', 'direct_report'],
      dtype='object')
```

# docker setup

* metabase admin
  * user: kyle_zeeuwen@gmail.com
  * password: not_secure1

* connecting metabase to mysql
  * docker compise has a link that names mysql host as `mysql`
  * need to add `allowPublicKeyRetrieval=true` to connection settings options to workaround `RSA public key is not available client side (option serverRsaPublicKeyFile not set)` error  
