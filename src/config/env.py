import os
import time

# TODO fail when required params not specified

DEFAULT_MODEL_NAME = 'DEFAULT_MODEL'
DEFAULT_MODEL_TEST_PROPORTION = 0.2
DEFAULT_MODEL_VERBOSITY = 4
DEFAULT_MODEL_PARALLELISM = 8
DEFAULT_SAMPLE_RATE = 1

# model
MODEL_TIMESTAMP = int(time.time())
MODEL_NAME = os.getenv('MODEL_NAME', DEFAULT_MODEL_NAME)
MODEL_TEST_PROPORTION = float(os.getenv('MODEL_TEST_PROPORTION', DEFAULT_MODEL_TEST_PROPORTION))
MODEL_VERBOSITY = int(os.getenv('MODEL_VERBOSITY', DEFAULT_MODEL_VERBOSITY))
MODEL_PARALLELISM = int(os.getenv('MODEL_PARALLELISM', DEFAULT_MODEL_PARALLELISM))

# file system
CONFIG_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(CONFIG_DIR, '..')
DATA_DIR = os.path.join(SRC_DIR, 'data')
MESSAGES_FILEPATH = os.path.join(DATA_DIR, 'input', 'disaster_messages.csv')
CATEGORIES_FILEPATH = os.path.join(DATA_DIR, 'input', 'disaster_categories.csv')
MODEL_DIRPATH = os.getenv('MODEL_DIRPATH')
SQLITE_FILEPATH = os.path.join(DATA_DIR, 'output', 'DisasterResponse.db')  # not used when DATABASE_TYPE = 'mysql'

# database
DATABASE_TYPE = 'mysql'
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')

# TRAINING
SAMPLE_RATE = float(os.getenv('SAMPLE_RATE', DEFAULT_SAMPLE_RATE))
