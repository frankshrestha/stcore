from .utils import _get_cnx_params

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool


def _get_cnx(endpoint=None, database=None):

    user, password, host, port, database = _get_cnx_params(endpoint, database)

    DB_URL = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'

    return create_engine(DB_URL, poolclass=NullPool).connect()


def get_reader_cnx(database=None):
    return _get_cnx('READER', database)


def get_writer_cnx(database=None):
    return _get_cnx('WRITER', database)
