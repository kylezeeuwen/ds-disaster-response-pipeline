from sqlalchemy import create_engine

from config.env import DATABASE_TYPE, MYSQL_HOST, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD, SQLITE_FILEPATH

def get_engine():
    if DATABASE_TYPE == 'sqlite':
        return create_engine(f"sqlite:///{SQLITE_FILEPATH}")
    elif DATABASE_TYPE == 'mysql':
        return create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}")
    else:
        raise Exception(f"Invalid engine type {DATABASE_TYPE}. Must by sqlite or mysql")
