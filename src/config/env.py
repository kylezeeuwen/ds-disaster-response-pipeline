import os
import time

# TODO fail when required params not specified

# file system
CONFIG_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(CONFIG_DIR, '..')
DATA_DIR = os.path.join(SRC_DIR, 'data')
MESSAGES_FILEPATH = os.path.join(DATA_DIR, 'input', 'disaster_messages.csv')
CATEGORIES_FILEPATH = os.path.join(DATA_DIR, 'input', 'disaster_categories.csv')
MODEL_DIRPATH = os.getenv('MODEL_DIRPATH')
SQLITE_FILEPATH = os.path.join(DATA_DIR, 'output', 'DisasterResponse.db') # not used when DATABASE_TYPE = 'mysql'

# database
DATABASE_TYPE = 'mysql'
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')

# model
MODEL_NAME = os.getenv('MODEL_NAME')
MODEL_TIMESTAMP = int(time.time())

#TRAINING
SAMPLE_RATE = float(os.getenv('SAMPLE_RATE'))

