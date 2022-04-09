import os
import pandas as pd
import joblib
import pickle

from lib.database import get_engine
from config.env import MODEL_DIRPATH, MODEL_NAME, MODEL_TIMESTAMP, SAMPLE_RATE


def save_model(model, metrics, model_parameters):
    '''
    INPUT:
    model - a trained scikit-learn model
    metrics - list - list of classification performance metrics for the model. Each list item is a dict containing:
      * model - string - model identifier - NAME-TIMESTAMP
      * category - string - the classification category that the metric describes
      * metric - string - the name of the metric. Currently (P, , N , TP , FP , TN , FN , TPR , TNR , PPV , NPV , ACC)
      * value - float - the value of the metric
    model_parameters - dict
      * parameter_candidates: the parameter set passed to Gridsearch to evaluate
      * parameters: the parameter combo that GridSearch selected as the best parameters

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
    metadata['MODEL_PARAMETERS'] = model_parameters

    with open(latest_model_filepath, 'wb') as f:
        pickle.dump({'model': model, 'metadata': metadata}, f)

    with open(timestamped_model_filepath, 'wb') as f:
        pickle.dump({'model': model, 'metadata': metadata}, f)

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
        filepath = os.path.join(MODEL_DIRPATH, filename)
        unpickled = joblib.load(filepath)

        (model, metadata) = (unpickled.get('model'), unpickled.get('metadata'))
        return (model, metadata)
    except Exception:
        print(Exception)
