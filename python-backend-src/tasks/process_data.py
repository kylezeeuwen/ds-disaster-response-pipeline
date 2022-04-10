import pandas as pd

from config.env import MESSAGES_FILEPATH, CATEGORIES_FILEPATH
from lib.database import get_engine

def process_data():
    '''
    INPUT:
    None

    OUTPUT:
    None

    Entry point called from main.py. Steps:
      * Load csv with classified disaster messages,
      * perform basic transform,
      * save messages to training_messages table in MySQL database
    '''

    print('Loading data from CSV')
    df = load_data(MESSAGES_FILEPATH, CATEGORIES_FILEPATH)

    print('Cleaning data')
    df = clean_data(df)

    engine = get_engine()

    print('Saving data')
    save_data(df, engine)

    print('Cleaned data saved to database!')
    test_data(engine)

def load_data(messages_filepath, categories_filepath):
    '''
    INPUT:
    messages_filepath - string - absolute file system path to messages CSV file
    categories_filepath - string - absolute file system path to categories CSV file

    OUTPUT:
    combined - pandas Dataframe - dataframe, one row per message,
      with 36 classifications in a single 'categories' column

    Load the two CSV files and combine into a single pandas dataframe
    '''

    messages = pd.read_csv(messages_filepath)
    categories_raw = pd.read_csv(categories_filepath)
    combined = messages.merge(categories_raw, how='left', on=['id'])
    return combined


def clean_data(df):
    '''
    INPUT:
    df - pandas Dataframe -  the datafrom from load_data containing one row per message,
      with 36 classifications in a single 'categories' column

    OUTPUT:
    df - pandas Dataframe - transformed dataframe, containing colums:
      * id : unique numeric message identifier
      * message : message translated to English
      * original : original untranslated message
      * genre : (direct|social|news) source of message
      * one column per 36 classifications : value is (0|1)

    The following transform steps are performed:
      * the cell format of categories column is {category1-name}-{category1-value};{category2-name}-{category2-value}.
        * extract out the category names, and create one column per category, with a [0|1] as the cell value
        * drop original categories column
      * drop duplicates
    '''

    # category cell format : {category1-name}-{category1-value};{category2-name}-{category2-value}...

    # create a dataframe of the 36 individual category columns
    categories = df['categories'].str.split(pat=';', expand=True)

    # extract the category names to use to name the columns in the categories dataframe
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
    '''
    INPUT:
    df - pandas Dataframe - the datafrom from clead_data containing one row per message, with 36 classification columns
    engine - SQLAlchemy DB engine

    OUTPUT:
    None

    save the df contents into the training_messages column in the MySQL database
    '''

    df.to_sql('training_messages', engine, index=False, if_exists='replace')


def test_data(engine):
    '''
    INPUT:
    engine - SQLAlchemy DB engine

    OUTPUT:
    None

    Perform basic tests to verify data was loaded
    '''

    record_count = engine.execute("SELECT count(*) AS c FROM training_messages").fetchall()[0][0]
    print(f"record count: {record_count}")
