import os
import time

# Ive chosen a flat model for passing config to libs: let the lib directly access the config.
# + lends itself to an IOC model, which I have not implemented in this small project
# + makes early iterations much easier.
# + keeps function argument length lower 🤘
# - This would cause code scaling and testing issues.

DEFAULT_MODEL_NAME = 'DEFAULT_MODEL'
DEFAULT_PARAMETER_SET = 'KNOWN_GOOD'
DEFAULT_MODEL_TEST_PROPORTION = 0.2
DEFAULT_MODEL_VERBOSITY = 4
DEFAULT_MODEL_PARALLELISM = 8
DEFAULT_SAMPLE_RATE = 1

# model
MODEL_TIMESTAMP = int(time.time())
MODEL_NAME = os.getenv('MODEL_NAME', DEFAULT_MODEL_NAME)
PARAMETER_SET = os.getenv('PARAMETER_SET', DEFAULT_PARAMETER_SET)
MODEL_TEST_PROPORTION = float(os.getenv('MODEL_TEST_PROPORTION', DEFAULT_MODEL_TEST_PROPORTION))
MODEL_VERBOSITY = int(os.getenv('MODEL_VERBOSITY', DEFAULT_MODEL_VERBOSITY))
MODEL_PARALLELISM = int(os.getenv('MODEL_PARALLELISM', DEFAULT_MODEL_PARALLELISM))

# file system
LIB_DIR = os.path.dirname(os.path.realpath(__file__))
WORKSPACE_DIR = os.path.join(LIB_DIR, '..')
CSV_DIR = os.path.join(WORKSPACE_DIR, './data')
MODEL_DIR = os.path.join(WORKSPACE_DIR, './models')
MESSAGES_FILEPATH = os.path.join(CSV_DIR, 'disaster_messages.csv')
CATEGORIES_FILEPATH = os.path.join(CSV_DIR, 'disaster_categories.csv')
SQLITE_PATH = os.path.join(WORKSPACE_DIR, './data/DisasterResponse.db')
APP_DIST_PATH = os.path.join(WORKSPACE_DIR, './app/dist')

# database
DATABASE_TYPE = 'sqlite'
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')

# TRAINING
SAMPLE_RATE = float(os.getenv('SAMPLE_RATE', DEFAULT_SAMPLE_RATE))
