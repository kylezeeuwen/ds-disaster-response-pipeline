import os
import joblib
import pickle

# TODO: Add to NOTES 👇
# Ive chosen a flat model for passing config to libs: let the lib directly access the config.
# Will have scaling issues but makes early iterations easier.
# Lends itself to an IOC model.
# Keeps function argument length lower 🤘

from config.env import MODEL_DIRPATH, MODEL_NAME, MODEL_TIMESTAMP, SAMPLE_RATE

# TODO add mechanism to select model using specific timestamp
def save_model(model, model_parameters):
    latest_model_filepath = os.path.join(MODEL_DIRPATH, f"{MODEL_NAME}-latest.pkl")
    timestamped_model_filepath = os.path.join(MODEL_DIRPATH, f"{MODEL_NAME}-{MODEL_TIMESTAMP}.pkl")

    metadata = {}
    metadata['SAMPLE_RATE'] = SAMPLE_RATE
    metadata['MODEL_NAME'] = MODEL_NAME
    metadata['MODEL_TIMESTAMP'] = MODEL_TIMESTAMP
    metadata['MODEL_PARAMETERS'] = model_parameters

    with open(latest_model_filepath, 'wb') as f:
        pickle.dump({ 'model': model, 'metadata': metadata }, f)

    with open(timestamped_model_filepath, 'wb') as f:
        pickle.dump({ 'model': model, 'metadata': metadata }, f)

def load_model():
    latest_model_filepath = os.path.join(MODEL_DIRPATH, f"{MODEL_NAME}-latest.pkl")
    unpickled = joblib.load(latest_model_filepath)

    (model, metadata) = (unpickled.get('model'), unpickled.get('metadata'))
    print(f"SAMPLE_RATE={metadata.get('SAMPLE_RATE')}")
    print(f"MODEL_NAME={metadata.get('MODEL_NAME')}")
    print(f"MODEL_TIMESTAMP={metadata.get('MODEL_TIMESTAMP')}")
    print(f"MODEL_PARAMETERS={metadata.get('MODEL_PARAMETERS')}")
    return (model, metadata)
