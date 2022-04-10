from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from lib.tokenizer import basic_english_stopword_lemmatise_tokeniser

parameter_sets = {

    # based on previous runs we know these are a good set for the data and chosen classifier
    'KNOWN_GOOD': {
        'features__text_pipeline__vect__ngram_range': ((1, 2),),
        'features__text_pipeline__vect__min_df': (0.0001,),
        'features__text_pipeline__vect__max_df': (0.5,),
        'features__text_pipeline__vect__max_features': (5000,),
        'features__text_pipeline__tfidf__use_idf': (True,),
    },

    'FULL': {
        'features__text_pipeline__vect__ngram_range': ((1, 1), (1, 2), (1, 3)),
        'features__text_pipeline__vect__min_df': (0.0001, 0.001, 0.01),
        'features__text_pipeline__vect__max_df': (0.5, 0.75, 0.9, 1.0),
        'features__text_pipeline__vect__max_features': (100, 1000, 5000, None),
        'features__text_pipeline__tfidf__use_idf': (True, False),
    },

    # TEST set - quick just prove the pipeline is working
    'TEST': {
        'features__text_pipeline__vect__ngram_range': ((1, 2), ),
        'features__text_pipeline__vect__min_df': (0.00001, ),
        'features__text_pipeline__vect__max_df': (0.5, ),
        'features__text_pipeline__vect__max_features': (100, ),
        'features__text_pipeline__tfidf__use_idf': (True, ),
    }

    # NOT WORKING
    # 'clf__n_estimators': [50, 100, 200],
    # 'clf__min_samples_split': [2, 3, 4],
    # 'features__transformer_weights': (
    #     {'text_pipeline': 1, 'starting_verb': 0.5},
    #     {'text_pipeline': 0.5, 'starting_verb': 1},
    #     {'text_pipeline': 0.8, 'starting_verb': 1},
    # )
}

def get_model(parameter_set, log_verbosity, parallelism):
    '''
    INPUT:
    parameter_set - string - the name of the parameter set (defined in model_factory.py) to use for the grid search
    log_verbosity - int - higher number → more logging from Gridsearch
    parallelism - int - number of simultaneous workers used by Gridsearch.
      * As a guideline this should be set to no higher than num CPU cores - 1

    OUTPUT:
      gridsearch instance ready to be run

    Specify the Gridsearch pipeline and the parameters to serarch accross
    '''

    if parameter_set not in parameter_sets:
        raise Exception(f"Unrecognised parameter_set {parameter_set}. Valid options are {parameter_sets.keys()}")

    pipeline = Pipeline([
        ('features', FeatureUnion([

            ('text_pipeline', Pipeline([
                ('vect', CountVectorizer(tokenizer=basic_english_stopword_lemmatise_tokeniser)),
                ('tfidf', TfidfTransformer())
            ])),

            # ('starting_verb', StartingVerbExtractor())
        ])),

        ('clf', MultiOutputClassifier(RandomForestClassifier()))
    ])

    return GridSearchCV(pipeline, param_grid=parameter_sets[parameter_set], verbose=log_verbosity, n_jobs=parallelism)
