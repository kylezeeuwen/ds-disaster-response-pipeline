import os
import pandas as pd
from sklearn.model_selection import train_test_split

from lib.database import get_engine
from lib.model_factory import get_model
from lib.model_repository import save_model

# TODO pull from DB
category_names = [
    'related',
    'request',
    'offer',
    'aid_related',
    'medical_help',
    'medical_products',
    'search_and_rescue',
    'security',
    'military',
    'child_alone',
    'water',
    'food',
    'shelter',
    'clothing',
    'money',
    'missing_people',
    'refugees',
    'death',
    'other_aid',
    'infrastructure_related',
    'transport',
    'buildings',
    'electricity',
    'tools',
    'hospitals',
    'shops',
    'aid_centers',
    'other_infrastructure',
    'weather_related',
    'floods',
    'storm',
    'fire',
    'earthquake',
    'cold',
    'other_weather',
    'direct_report'
]

# TODO from config
sample_rate=1

def load_data():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM training_messages", engine)
    df =df.sample(frac=sample_rate)

    X = df['message']
    Y = df[category_names]

    return (X, Y, category_names)

#  TODO more detail in evaluate_mode
def evaluate_model(model, X_test, Y_test, category_names):
    Y_pred = model.predict(X_test)

    accuracy = (Y_pred == Y_test).mean()
    print("Accuracy:", accuracy)

    # print("Labels:", labels)
    # confusion_mat = confusion_matrix(Y_test, Y_pred)
    # print("Confusion Matrix:\n", confusion_mat)

    return Y_pred

def train_classifier():

    print(f"Loading data...")
    X, Y, category_names = load_data()
    # TODO test_size from config
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

    # TODO from config
    log_verbosity=4
    parallelism=8
    parameters={}

    print('Building model...')
    model = get_model(parameters, log_verbosity, parallelism)

    print('Training model...')
    model.fit(X_train, Y_train)
    print("\nBest Parameters:", model.best_params_)

    print('Evaluating model...')
    Y_pred = evaluate_model(model, X_test, Y_test, category_names)

    print('Saving model...')
    save_model('model1', model, parameters)

    print('Trained model saved!')
