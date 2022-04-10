from sqlalchemy import create_engine, text

from config.env import MYSQL_HOST, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD

def get_engine():
    '''
    INPUT:
    None

    OUTPUT:
    engine - a SQLAlchemy MySQL engine for connecting to the database
    '''

    return create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}")

def run_query(query_text):
    with get_engine().begin() as conn:
        qry = text(query_text)
        resultset = conn.execute(qry)
        return [x._asdict() for x in resultset]
