import os
import pandas as pd
import joblib
import pickle

from lib.database import get_engine
from config.env import MODEL_DIRPATH, MODEL_NAME, MODEL_TIMESTAMP, SAMPLE_RATE


def save_model(
    model,
    metrics=[],
    train_set_size=None,
    test_set_size=None,
    chosen_parameters={},
):
    '''
    TODO: update docstring with new params
    INPUT:
    model - a trained scikit-learn model
    metrics - list - list of classification performance metrics for the model. Each list item is a dict containing:
      * model - string - model identifier - NAME-TIMESTAMP
      * category - string - the classification category that the metric describes
      * metric - string - the name of the metric. Currently (P, , N , TP , FP , TN , FN , TPR , TNR , PPV , NPV , ACC)
      * value - float - the value of the metric
    train_set_size - int - number of samples in the training set
    test_set_size - int - number of samples in the test set
    chosen_parameters - dict - the parameter combo that GridSearch selected as the best parameters

    OUTPUT:
    None

    Save model and metadata to local filesystem as a pickle file and save metrics to database
    '''

    latest_model_filepath = os.path.join(MODEL_DIRPATH, f"{MODEL_NAME}-latest.pkl")
    timestamped_model_filepath = os.path.join(MODEL_DIRPATH, f"{MODEL_NAME}-{MODEL_TIMESTAMP}.pkl")

    metadata = {}
    metadata['SAMPLE_RATE'] = SAMPLE_RATE
    metadata['MODEL_NAME'] = MODEL_NAME
    metadata['MODEL_TIMESTAMP'] = MODEL_TIMESTAMP
    metadata['CHOSEN_PARAMETERS'] = chosen_parameters
    metadata['TRAIN_SET_SIZE'] = train_set_size
    metadata['TEST_SET_SIZE'] = test_set_size

    print(f"best score {model.best_score_}")
    print(f"best index {model.best_index_}")

    with open(latest_model_filepath, 'wb') as f:
        pickle.dump({'model': model.best_estimator_, 'metadata': metadata}, f)

    with open(timestamped_model_filepath, 'wb') as f:
        pickle.dump({'model': model.best_estimator_, 'metadata': metadata}, f)

    engine = get_engine()
    metrics_df = pd.DataFrame(metrics)
    metrics_df.to_sql('model_metrics', engine, index=False, if_exists='append')

# TODO add mechanism to select model using specific timestamp
def load_model(model_name=MODEL_NAME):
    '''
    Wrapper for _load_model below that handles the file naming convention of MODELNAME-MODELTIMESTAMP.pkl
    '''

    latest_model_filename = f"{model_name}-latest.pkl"
    return _load_model(latest_model_filename)


def _load_model(filename):
    '''
    INPUT:
    filename - the filename of the model to load - including the .pkl extension

    OUTPUT: tuple containing
    model - scikit-learn model - object that was retrieved from a pickle file on the local filesystem
    metadata - dict - key value pairs describing the model

    Return model and metadata based on filename
    '''
    try:
        import sys
        from datetime import datetime
        filepath = os.path.join(MODEL_DIRPATH, filename)
        print(datetime.now())
        print(sys.argv, flush=True)
        print(filepath, flush=True)
        unpickled = joblib.load(filepath)


        (model, metadata) = (unpickled.get('model'), unpickled.get('metadata'))
        return (model, metadata)
    except Exception:
        print(Exception)
