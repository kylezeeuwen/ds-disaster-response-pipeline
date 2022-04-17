from flask import Flask, render_template, request, g
from flask_cors import CORS

import pandas as pd

from lib.env import MODEL_NAME, APP_DIST_PATH
from lib.database import get_engine, run_query
from lib.model_repository import load_model

(model, metadata) = load_model()  # NB model name specified in ENV

engine = get_engine()
df = pd.read_sql_table('category', engine)
all_categories = df['category'].tolist()

# the /react-build path is provided via the docker-compose that maps docker-data/react-build to /react-build
app = Flask(__name__, static_url_path='', static_folder=APP_DIST_PATH)
CORS(app)

def flask_app():
    '''
    INPUT:
    None

    OUTPUT:
    None

    Entry point called from main.py. Start the app listening on port 5000 for incoming requests
    '''
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

@app.route('/')
def root():
    '''serve index.html when / is requested'''

    return app.send_static_file('index.html')

@app.route("/api/get-model-info")
def get_model_info():
    '''
    INPUT:
    None

    OUTPUT: VIA JSON object
    metadata - dict - metadata containing model info such as name, timestamp, candidate parameters, chosen parameters

    Return metadata about the currently loaded model
    '''

    return metadata


@app.route("/api/get-categories")
def get_categories():
    '''
    INPUT:
    None

    OUTPUT: VIA JSON object
    categories - list - list of the categories that the currently loaded model classified messages into

    Return metadata about the currently loaded model
    '''

    return {"categories": all_categories}


@app.route("/api/get-model-performance")
def get_model_performance():
    '''
    INPUT:
    None

    OUTPUT: VIA JSON object
    metrics - list - list of dicts. Each list item is a dict containing:
      * model - string - model identifier - NAME-TIMESTAMP
      * category - string - the classification category that the metric describes
      * metric - string - the name of the metric. Currently (P, , N , TP , FP , TN , FN , TPR , TNR , PPV , NPV , ACC)
      * value - float - the value of the metric

    Return metrics about the currently loaded model
    '''

    # TODO this method for determining the results of the latest model is hacky
    metrics = run_query(f"SELECT * FROM model_metrics where model = (SELECT MAX(model) FROM model_metrics WHERE model like '{MODEL_NAME}-%')")
    return {'metrics': metrics }

# NB TODO there is no guarantee the model or the all_categories is loaded


@app.route("/api/classify", methods=['POST'])
def classify():
    '''
    INPUT: (VIA POST body)
    message - string - the message to classify

    OUTPUT: VIA JSON object
    message - string - the message to classify
    classifications - dict - fields are categories, values are (0|1)

    Classify the message using the currently loaded model
    '''

    request_json = request.json
    message = request_json.get('message', '')

    classification_labels_int64 = model.predict([message])[0]
    classification_labels = [int(x) for x in classification_labels_int64]
    classification_results = dict(zip(all_categories, classification_labels))

    return {
        'message': message,
        'classifications': classification_results,
    }

if __name__ == '__main__':
    flask_app()