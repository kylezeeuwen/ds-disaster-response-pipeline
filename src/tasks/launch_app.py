import os
import json
import plotly
import pandas as pd

from flask import Flask
from flask import render_template, request, jsonify

from lib.model_repository import load_model
(model, metadata) = load_model('model1')

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'web_templates'))
print('here')
print(template_dir)
app = Flask(__name__, template_folder=template_dir)

# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    # TODO: Below is an example - modify to extract data for your own visuals

    # create visuals
    # TODO: Below is an example - modify to create your own visuals
    graphs = [
    ]
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # load data
    from lib.database import get_engine
    engine = get_engine()
    # TODO get category_names not trainin messages
    df = pd.read_sql_table('training_messages', engine)

    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    print(classification_results)

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )

def launch_app():
    app.run(host='0.0.0.0', port=5000, debug=True)
