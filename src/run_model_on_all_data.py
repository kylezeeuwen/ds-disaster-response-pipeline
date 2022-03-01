
import pandas as pd
from sqlalchemy import create_engine
import re
import joblib

# TODO move to config
sample_rate = 1

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
def conditionally_download_nltk_package (lookup_name, download_name):
    try:
        nltk.data.find(lookup_name)
    except LookupError:
        print(f"downloading nltk {download_name}")
        nltk.download(download_name)

conditionally_download_nltk_package('tokenizers/punkt', 'punkt')
conditionally_download_nltk_package('stopwords', 'stopwords')
conditionally_download_nltk_package('wordnet', 'wordnet')
conditionally_download_nltk_package('omw-1.4', 'omw-1.4')


# TODO deduplicate this. Need this here to unpickle
english_stopwords = stopwords.words("english")
def my_tokenize(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9]", " ", text)
    words = word_tokenize(text)
    words = [w for w in words if w not in english_stopwords]
    words = [WordNetLemmatizer().lemmatize(w) for w in words]

    return words

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

# TODO dedupe and move to lib
from operator import itemgetter
def get_engine(engine_type, connection_details):
    if engine_type == 'sqlite':
        filepath = itemgetter('filepath')(connection_details)
        return create_engine(f"sqlite:///{filepath}")
    elif engine_type == 'mysql':
        username, password, hostname, databasename = itemgetter('username', 'password', 'hostname', 'databasename')(connection_details)
        return create_engine(f"mysql+pymysql://{username}:{password}@{hostname}/{databasename}")
    else:
        raise Exception(f"Invalid engine type {engine_type}. Must by sqlite or mysql")

def _get_engine():
    engine_type = 'mysql'
    return get_engine(engine_type, {
        'username': 'disaster_response',
        'password': 'disaster_response',
        'hostname': '127.0.0.1',
        'databasename': 'disaster_response'
    })

def load_data():
    engine = _get_engine()
    df = pd.read_sql("SELECT * FROM training_messages", engine, index_col='id')
    df =df.sample(frac=sample_rate)

    X = df['message']
    Y = df[category_names]

    return (X, Y, category_names)

def main():

    # TODO use relative to filepath not workingpath
    model = joblib.load("./src/models/classifier.pkl")
    sql_engine = _get_engine()


    print(f"Loading full corpus")
    X, Y_actual, category_names = load_data()

    print('Running model...')
    Y_predicted = model.predict(X)

    print('Writing results to database')

    Y_actual\
        .stack()\
        .to_frame()\
        .reset_index()\
        .rename(columns={ 'level_0': 'id', 'level_1': 'category', 0: 'score' })\
        .to_sql('classification', sql_engine, index=False, if_exists='replace')

    results = pd.DataFrame(data=Y_predicted, index=X.index, columns=category_names)\
        .assign(id = X.index)\
        .assign(timestamp = pd.Timestamp.now())

    results.to_sql('result_wide', sql_engine, index=False, if_exists='replace')

    results.stack()\
        .to_frame()\
        .reset_index()\
        .rename(columns={ 'level_0': 'id', 'level_1': 'category', 0: 'score' })\
        .assign(timestamp = pd.Timestamp.now())\
        .to_sql('result', sql_engine, index=False, if_exists='replace')

    pd.Series(category_names, name='category')\
        .to_sql('category', sql_engine, index=False, if_exists='replace')

    with sql_engine.connect() as conn:
        conn.execute("DROP TABLE IF EXISTS result_summary")
        conn.execute("""
            CREATE TABLE result_summary
            SELECT
              *,
              IF(P = 0, 0, TP / P) AS TPR,
              IF(N = 0, 0, TN / N) AS TNR,
              IF((TP+FP) = 0, 0, TP / (TP + FP)) AS PPV,
              IF((TN + FN) = 0, 0, TN / (TN + FN)) AS NPV,
              IF((P + N) = 0, 0, (TP + TN) / (P + N)) AS ACC
            FROM (
              SELECT
                C.category,
                COUNT(DISTINCT id) records,
                COUNT(DISTINCT IF(X.score = 1, id, null)) as P,
                COUNT(DISTINCT IF(X.score = 0, id, null)) as N,
                COUNT(DISTINCT IF(Y.score = 1, id, null)) as P_predicted,
                COUNT(DISTINCT IF(Y.score = 0, id, null)) as N_predicted,
                COUNT(DISTINCT IF(X.score = 1 AND Y.score = 1, id, null)) as TP,
                COUNT(DISTINCT IF(X.score = 0 AND Y.score = 1, id, null)) as FP,
                COUNT(DISTINCT IF(X.score = 0 AND Y.score = 0, id, null)) as TN,
                COUNT(DISTINCT IF(X.score = 1 AND Y.score = 0, id, null)) as FN
              FROM category C
                     JOIN classification X USING (category)
                     JOIN result Y USING (id, category)
              GROUP BY C.category
            ) stats_l0;        
        """)

if __name__ == '__main__':
    main()