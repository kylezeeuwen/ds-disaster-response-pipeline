from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC

from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from lib.tokenizer import basic_english_stopword_lemmatise_tokeniser
from lib.evaluate_model import custom_f1_scorer_with_recall_favored
from sklearn.metrics import make_scorer

wrapped_custom_f1_scorer_with_recall_favored = make_scorer(custom_f1_scorer_with_recall_favored)

parameter_set_parts = {
    # based on previous runs we know these are a good set for the data and chosen classifier
    'TEXT_PIPELINE_KNOWN_GOOD': {
        'features__text_pipeline__vect__ngram_range': ((1, 2),),
        'features__text_pipeline__vect__min_df': (0.0001,),
        'features__text_pipeline__vect__max_df': (0.5,),
        'features__text_pipeline__vect__max_features': (5000,),
        'features__text_pipeline__tfidf__use_idf': (True,),
    },
    'TEXT_PIPELINE_FULL': {
        'features__text_pipeline__vect__ngram_range': ((1, 1), (1, 2), (1, 3)),
        'features__text_pipeline__vect__min_df': (0.0001, 0.001, 0.01),
        'features__text_pipeline__vect__max_df': (0.5, 0.75, 0.9, 1.0),
        'features__text_pipeline__vect__max_features': (100, 1000, 5000, None),
        'features__text_pipeline__tfidf__use_idf': (True, False),
    },

    # TEST set - quick just prove the pipeline is working
    'TEXT_PIPELINE_TEST': {
        'features__text_pipeline__vect__ngram_range': ((1, 2), ),
        'features__text_pipeline__vect__min_df': (0.00001, ),
        'features__text_pipeline__vect__max_df': (0.5, ),
        'features__text_pipeline__vect__max_features': (100, ),
        'features__text_pipeline__tfidf__use_idf': (True, ),
    },

    'RANDOM_FOREST_FULL': {
        'clf': (MultiOutputClassifier(RandomForestClassifier()), ),
        # hyper params grid from Will Koehrson blog https://towardsdatascience.com/28d2aa77dd74
        'clf__estimator__max_depth': (10, 25, 50, 75, 100, None),
        'clf__estimator__max_features': ('auto', 'sqrt'),
        'clf__estimator__n_estimators': (200, 400, 800, 1200, 1600, 2000),
        'clf__estimator__min_samples_split': (2, 5, 10),
        'clf__estimator__min_samples_leaf': (1, 2, 4),
        'clf__estimator__bootstrap': (True, False),
        # ignoring these params : ( 'clf__criterion', 'clf__max_leaf_nodes', 'clf__min_impurity_decrease', 'clf__min_impurity_split', 'clf__min_weight_fraction_leaf', 'clf__n_jobs', 'clf__oob_score', 'clf__warm_start' )
    },

    'DECISION_TREE_FULL': {
        'clf': (MultiOutputClassifier(DecisionTreeClassifier()), ),
        # param suggestions from https://www.projectpro.io/recipes/optimize-hyper-parameters-of-decisiontree-model-using-grid-search-in-python
        'clf__estimator__criterion': ('gini', 'entropy'),
        'clf__estimator__max_depth': (2, 4, 6, 8, 10, 12),
    },

    'LINEAR_SVC_FULL': {
            'clf': (MultiOutputClassifier(LinearSVC()), ),
            # param suggestions from https://medium.com/swlh/4d17671d1ed2
            'clf__estimator__C': (0.1, 1, 100, 1000),
            # 'kernel':('rbf','poly','sigmoid','linear'), #NB disabled as LinearSVM implies linear kernel
            'clf__estimator__degree': (1, 2, 3, 4, 5, 6),
            'clf__estimator__gamma': (1, 0.1, 0.01, 0.001, 0.0001),
    }
}



parameter_sets = {
    'KNOWN_GOOD': parameter_set_parts['TEXT_PIPELINE_KNOWN_GOOD'],
    'FULL': parameter_set_parts['TEXT_PIPELINE_FULL'],
    'TEST': parameter_set_parts['TEXT_PIPELINE_TEST'],

    'FULL_MULTI_PIPELINE_EXHAUSTIVE': [
        parameter_set_parts['TEXT_PIPELINE_KNOWN_GOOD'] | parameter_set_parts['RANDOM_FOREST_FULL'],
        parameter_set_parts['TEXT_PIPELINE_KNOWN_GOOD'] | parameter_set_parts['DECISION_TREE_FULL'],
        parameter_set_parts['TEXT_PIPELINE_KNOWN_GOOD'] | parameter_set_parts['LINEAR_SVC_FULL'],
    ]
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

    param_grid = parameter_sets[parameter_set]

    return GridSearchCV(
        pipeline,
        param_grid=param_grid,
        verbose=log_verbosity,
        n_jobs=parallelism,
        # scoring=f1_scorer_with_recall_favored,
        scoring=wrapped_custom_f1_scorer_with_recall_favored
    )
