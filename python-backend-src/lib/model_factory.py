from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from lib.tokenizer import basic_english_stopword_lemmatise_tokeniser

def get_model(parameters, log_verbosity, parallelism):
    '''
    INPUT:
    parameter - dict - the parameter options for GridSearch to iterate
    log_verbosity - int - higher number → more logging from Gridsearch
    parallelism - int - number of simultaneous workers used by Gridsearch.
      * As a guideline this should be set to no higher than num CPU cores - 1

    OUTPUT:
      gridsearch instance ready to be run

    Specify the Gridsearch pipeline and the parameters to serarch accross
    '''

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

    return GridSearchCV(pipeline, param_grid=parameters, verbose=log_verbosity, n_jobs=parallelism)
