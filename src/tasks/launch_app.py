from flask import Flask, render_template, request, g
from flask_cors import CORS

import pandas as pd

# TODO this should be abstracted
from sqlalchemy import text

from config.env import MODEL_NAME
from lib.database import get_engine
from lib.model_repository import list_models, load_model

# TODO to app init
(model, metadata) = load_model()  # NB model name specified in ENV

engine = get_engine()
df = pd.read_sql_table('category', engine)
all_categories = df['category'].tolist()

# the /react-web path is provided via the docker-compose that maps src/react-web/build to /my-app
app = Flask(__name__, static_url_path='', static_folder='/react-web', template_folder='/react-web')
CORS(app)


@app.route("/")
def hello():
    return render_template("index.html")

# TODO delete


@app.route("/api/models")
def models():
    models = list_models()
    return {"models": models}


@app.route("/api/get-model-info")
def get_model_info():
    return metadata


@app.route("/api/get-categories")
def get_categories():
    return {"categories": all_categories}


@app.route("/api/get-model-performance")
def get_model_performance():
    with engine.begin() as conn:
        # TODO this method for determining the results of the latest model is hacky
        qry = text(
            f"SELECT * FROM model_metrics where model = (SELECT MAX(model) FROM model_metrics WHERE model like '{MODEL_NAME}-%')")
        resultset = conn.execute(qry)
        results_as_dict = [x._asdict() for x in resultset]
        return {'metrics': results_as_dict}

# NB TODO there is no guarantee the model or the all_categories is loaded


@app.route("/api/classify", methods=['POST'])
def classify():
    request_json = request.json
    message = request_json.get('message', '')

    classification_labels_int64 = model.predict([message])[0]
    classification_labels = [int(x) for x in classification_labels_int64]
    classification_results = dict(zip(all_categories, classification_labels))

    return {
        'message': message,
        'classifications': classification_results,
    }


def launch_app():
    app.run(host='0.0.0.0', port=5000, debug=True)
