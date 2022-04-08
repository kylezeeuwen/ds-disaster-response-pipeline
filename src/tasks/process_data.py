import pandas as pd

from config.env import MESSAGES_FILEPATH, CATEGORIES_FILEPATH
from lib.database import get_engine

def load_data(messages_filepath, categories_filepath):
    messages = pd.read_csv(messages_filepath)
    categories_raw = pd.read_csv(categories_filepath)
    combined = messages.merge(categories_raw, how='left', on=['id'])
    return combined

def clean_data(df):
    # category cell format : {category1-name}-{category1-value};{category2-name}-{category2-value}...

    # create a dataframe of the 36 individual category columns
    categories = df['categories'].str.split(pat=';', expand=True)

    # extract the cateogry names to use to name the columns in the categories dataframe
    category_colnames = categories.iloc[0].apply(lambda x: x.split('-')[0])
    categories.columns = category_colnames

    # format the cells to just contain the 0 or 1 and convert type to numeric
    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].apply(lambda x: x[-1]).astype(int)

    # remove the raw categories string from the dataframe and add the formatted series
    df = df.drop(columns=['categories'])
    df = pd.concat([df, categories], axis=1)

    # deduplicate using the message
    df = df.drop_duplicates(subset=['message'], keep='first')

    return df

def save_data(df, engine):
    df.to_sql('training_messages', engine, index=False, if_exists='replace')

def test_data(engine):
    record_count = engine.execute("SELECT count(*) AS c FROM training_messages").fetchall()[0][0]
    print(f"record count: {record_count}")

def process_data():
    print('Loading data from CSV')
    df = load_data(MESSAGES_FILEPATH, CATEGORIES_FILEPATH)

    print('Cleaning data')
    df = clean_data(df)

    #TODO howto cleanly teardown connection on exit
    engine = get_engine()

    print('Saving data')
    save_data(df, engine)

    print('Cleaned data saved to database!')
    test_data(engine)
