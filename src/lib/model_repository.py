import os
from os import listdir
from os.path import isfile, join
import pandas as pd
import joblib
import pickle

# TODO: Add to NOTES 👇
# Ive chosen a flat model for passing config to libs: let the lib directly access the config.
# Will have scaling issues but makes early iterations easier.
# Lends itself to an IOC model.
# Keeps function argument length lower 🤘

from lib.database import get_engine
from config.env import MODEL_DIRPATH, MODEL_NAME, MODEL_TIMESTAMP, SAMPLE_RATE

# TODO add mechanism to select model using specific timestamp


def save_model(model, metrics, model_parameters):
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

    # TODO howto cleanly teardown connection on exit
    engine = get_engine()
    metrics_df = pd.DataFrame(metrics)
    metrics_df.to_sql('model_metrics', engine, index=False, if_exists='append')

# TODO not currently used


def list_models():
    model_list = []
    for filename in [f for f in listdir(MODEL_DIRPATH) if isfile(join(MODEL_DIRPATH, f))]:
        (model, metadata) = _load_model(filename)
        model_list.append(metadata)

    return model_list


def load_model(model_name=MODEL_NAME):
    latest_model_filename = f"{model_name}-latest.pkl"
    return _load_model(latest_model_filename)


def _load_model(filename):
    try:
        filepath = os.path.join(MODEL_DIRPATH, filename)
        unpickled = joblib.load(filepath)

        (model, metadata) = (unpickled.get('model'), unpickled.get('metadata'))
        return (model, metadata)
    except Exception:
        print(Exception)
