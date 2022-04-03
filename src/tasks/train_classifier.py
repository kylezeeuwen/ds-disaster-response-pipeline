import pandas as pd
from sklearn.model_selection import train_test_split

from config.env import SAMPLE_RATE, MODEL_VERBOSITY, MODEL_PARALLELISM, MODEL_TEST_PROPORTION

from lib.database import get_engine
from lib.model_factory import get_model
from lib.model_repository import save_model

def load_data():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM training_messages", engine)
    # TODO: could push to process_data
    # how to not corrupt DB with incomplete sample rate
    # could introduce DB WRITE SAMPLE RATE, TRAIN SAMPLE RATE, etc
    df =df.sample(frac=SAMPLE_RATE)

    category_names = pd.read_sql("SELECT * FROM category", engine)['category'].to_numpy()
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
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=MODEL_TEST_PROPORTION)

    # TODO where from ?
    parameters = {
        'features__text_pipeline__vect__ngram_range': ((1, 1), (1, 2)),
        'features__text_pipeline__vect__max_df': (0.5, 1.0),
        'features__text_pipeline__vect__max_features': (10, 100, 500, 1000),
        'features__text_pipeline__tfidf__use_idf': (True, False),

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

    print('Evaluating model...')
    Y_pred = evaluate_model(model, X_test, Y_test, category_names)

    print('Saving model...')
    save_model(model, {
      'parameter_candidates': parameters,
      'parameters': model.best_params_
    }) #NB model name specified in ENV

    print('Trained model saved!')
