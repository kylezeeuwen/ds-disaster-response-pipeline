from sqlalchemy import create_engine, text

from lib.env import MYSQL_HOST, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD, DATABASE_TYPE, SQLITE_PATH

def get_engine():
    '''
    INPUT:
    None

    OUTPUT:
    engine - a SQLAlchemy MySQL engine for connecting to the database
    '''

    if DATABASE_TYPE == 'sqlite':
        return create_engine(f"sqlite:///{SQLITE_PATH}")
    elif DATABASE_TYPE == 'mysql':
        return create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}")
    else:
        raise Exception(f"Unrecognised DATABASE_TYPE {DATABASE_TYPE}. Valid options are 'sqlite' or 'mysql'")

def run_query(query_text):
    with get_engine().begin() as conn:
        qry = text(query_text)
        resultset = conn.execute(qry)
        return [x._asdict() for x in resultset]

def run_statement(query_text):
    with get_engine().begin() as conn:
        qry = text(query_text)
        conn.execute(qry)
