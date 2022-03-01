import os
import joblib
import pickle

from config.env import MODEL_DIRPATH

def save_model(name, model, metadata):
    model_filepath = os.path.join(MODEL_DIRPATH, f"{name}.pkl")
    with open(model_filepath, 'wb') as f:
        pickle.dump({ 'model': model, 'metadata': metadata }, f)

def load_model(name):
    model_filepath = os.path.join(MODEL_DIRPATH, f"{name}.pkl")
    unpickled = joblib.load(model_filepath)
    return (unpickled.get('model'), unpickled.get('metadata'))
