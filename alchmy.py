from .utils import _get_cnx_params

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool


def _get_cnx(endpoint=None, database='', env_key_prefix=''):

    user, password, host, port, database = _get_cnx_params(
        endpoint, database, env_key_prefix)

    DB_URL = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'

    return create_engine(DB_URL, poolclass=NullPool).connect()


def get_reader_cnx(database='', env_key_prefix=''):
    return _get_cnx('READER', database, env_key_prefix)


def get_writer_cnx(database='', env_key_prefix=''):
    return _get_cnx('WRITER', database, env_key_prefix)
