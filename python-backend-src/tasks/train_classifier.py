import pandas as pd
from sklearn.model_selection import train_test_split

from config.env import SAMPLE_RATE, MODEL_NAME, MODEL_TIMESTAMP, MODEL_VERBOSITY, MODEL_PARALLELISM, MODEL_TEST_PROPORTION

from lib.database import get_engine
from lib.model_factory import get_model
from lib.model_repository import save_model

def train_classifier():
    '''
    INPUT:
    None

    OUTPUT:
    None

    Entry point called from main.py. Steps:
      * Load classified training messages
      * Split into train vs test set
      * Fit model using grid search and parameters specified below
      * Compute performance metrics
      * Save model to a pickle file and save metric to database
    '''

    print(f"Loading data...")
    X, Y, category_names = load_data()
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=MODEL_TEST_PROPORTION)

    parameters = {
        # APR 6 set - quicker run, comparable performance
        # 'features__text_pipeline__vect__ngram_range': ((1, 1), (1, 2)),
        # 'features__text_pipeline__vect__max_df': (0.5, 1.0),
        # 'features__text_pipeline__vect__max_features': (10, 100, 500, 1000),

        # APR 7 set - ran near 24 hours
        # 'features__text_pipeline__vect__ngram_range': ((1, 1), (1, 2), (1, 3)),
        # 'features__text_pipeline__vect__min_df': (0.0001, 0.001, 0.01),
        # 'features__text_pipeline__vect__max_df': (0.5, 0.75, 0.9, 1.0),
        # 'features__text_pipeline__vect__max_features': (100, 1000, 5000, None),
        # 'features__text_pipeline__tfidf__use_idf': (True, False),

        # TEST set - quick just prove the pipeline not broke
        'features__text_pipeline__vect__ngram_range': ((1, 1), ),
        'features__text_pipeline__vect__min_df': (0.00001, ),
        'features__text_pipeline__vect__max_df': (0.75, ),
        'features__text_pipeline__vect__max_features': (100, ),
        'features__text_pipeline__tfidf__use_idf': (True, ),


        # DISABLE FOR PERF REASONS
        # 'features__text_pipeline__vect__max_df': (0.5, 0.75, 1.0),
        # 'features__text_pipeline__vect__max_features': (None, 5000, 10000),
        # 'features__text_pipeline__tfidf__use_idf': (True, False),

        # NOT WORKING
        # 'clf__n_estimators': [50, 100, 200],
        # 'clf__min_samples_split': [2, 3, 4],
        # 'features__transformer_weights': (
        #     {'text_pipeline': 1, 'starting_verb': 0.5},
        #     {'text_pipeline': 0.5, 'starting_verb': 1},
        #     {'text_pipeline': 0.8, 'starting_verb': 1},
        # )
    }

    print('Building model...')
    model = get_model(parameters, MODEL_VERBOSITY, MODEL_PARALLELISM)

    print('Training model...')
    model.fit(X_train, Y_train)
    print("\nBest Parameters:", model.best_params_)

    # only save clf.best_estimator_ to save on pickle size
    #  https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html
    # explore scoring, multioutput classifiers, best_score_ and best_index_

    print('Evaluating model...')
    metrics = evaluate_model(model, X_test, Y_test, category_names)
    metrics.append({'model': f"{MODEL_NAME}-{MODEL_TIMESTAMP}", 'category': 'ALL',
                   'metric': 'train_set_size', 'value': len(X_train)})
    metrics.append({'model': f"{MODEL_NAME}-{MODEL_TIMESTAMP}", 'category': 'ALL',
                   'metric': 'test_set_size', 'value': len(X_test)})

    print('Saving model...')
    save_model(model, metrics, {
        'parameter_candidates': parameters,
        'parameters': model.best_params_,
    })  # NB model name specified in ENV

    print('Trained model saved!')

def load_data():
    '''
    INPUT:
    None

    OUTPUT:
    X - pandas Series - the messages to classify
    Y - pandas Dataframe - the classifications for the messages, each cell value is (0|1)
    category_names - list - list of categories to classify messages into

    Steps:
      * load the classified message corpus from the database
      * apply the sample rate (for development purposes to decrease run time) to reduce the corpus size
      * split the corpus into X and Y for ML training
    '''

    engine = get_engine()
    df = pd.read_sql("SELECT * FROM training_messages", engine)
    df = df.sample(frac=SAMPLE_RATE)

    category_names = pd.read_sql("SELECT * FROM category", engine)['category'].to_numpy()
    X = df['message']
    Y = df[category_names]

    return (X, Y, category_names)


def evaluate_model(model, X_test, Y_test, category_names):
    '''
    INPUT:
    model - a trained classifier
    X_test - pandas Series - messages to test classifier
    Y_test - pandas Dataframe - message classifications
    category_names - category name index for Y_test

    OUTPUT:
    metrics - list - list of classification performance metrics for the model. Each list item is a dict containing:
      * model - string - model identifier - NAME-TIMESTAMP
      * category - string - the classification category that the metric describes
      * metric - string - the name of the metric. Currently (P, , N , TP , FP , TN , FN , TPR , TNR , PPV , NPV , ACC)
      * value - float - the value of the metric

    Steps:
      * classify the test messages
      * for each category, compute a series of performance metrics
    '''

    Y_pred = model.predict(X_test)

    metrics = []
    for idx, category in enumerate(category_names):
        y_test_single_classification = Y_test[category].tolist()
        y_pred_single_classification = Y_pred[:, idx]
        single_classifier_metrics = evaluate_single_classifier(
            y_test_single_classification, y_pred_single_classification)

        for metric, value in single_classifier_metrics.items():
            metrics.append({
                'model': f"{MODEL_NAME}-{MODEL_TIMESTAMP}",
                'category': category,
                'metric': metric,
                'value': value
            })

    return metrics


def divide_or_zero(numerator, denominator):
    '''
    INPUT:
    numerator - numeric
    denominator - numeric

    OUTPUT:
    numeric

    Divide numerator by denominotor, unless denominator is 0 then just return 0
    '''
    return numerator / denominator if denominator != 0 else 0

def evaluate_single_classifier(y_actual, y_predictions):
    '''
    INPUT:
    y_actual - array - actual results
    y_predictions - array - predictions

    OUTPUT:
    metrics - a series of performance metrics
    '''

    TP = 0
    FP = 0
    TN = 0
    FN = 0
    P = 0
    N = 0

    for i in range(len(y_predictions)):
        if y_actual[i] == 1:
            P += 1
        if y_actual[i] == 0:
            N += 1
        if y_actual[i] == y_predictions[i] == 1:
            TP += 1
        if y_predictions[i] == 1 and y_actual[i] != y_predictions[i]:
            FP += 1
        if y_actual[i] == y_predictions[i] == 0:
            TN += 1
        if y_predictions[i] == 0 and y_actual[i] != y_predictions[i]:
            FN += 1

    # source: https://en.wikipedia.org/wiki/Sensitivity_and_specificity
    # sensitivity, recall, hit rate, or true positive rate (TPR)
    TPR = divide_or_zero(TP, P)

    # specificity, selectivity or true negative rate (TNR)
    TNR = divide_or_zero(TN, N)

    # precision or positive predictive value (PPV)
    PPV = divide_or_zero(TP, (TP + FP))

    # ____ or negative predictive value (PPV)
    NPV = divide_or_zero(TN, (TN + FN))

    # accuracy
    ACC = divide_or_zero((TP + TN), (P + N))

    return {
        "P": P,
        "N": N,
        "TP": TP,
        "FP": FP,
        "TN": TN,
        "FN": FN,
        "TPR": TPR,
        "TNR": TNR,
        "PPV": PPV,
        "NPV": NPV,
        "ACC": ACC,
    }
