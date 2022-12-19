import pymysql
from pymysql.connections import Connection
from pymysql.cursors import DictCursor

from .utils import _get_cnx_params


def _get_cnx(endpoint=None, database='', env_key_prefix='') -> Connection:
    user, password, host, port, database = _get_cnx_params(endpoint, database, env_key_prefix)

    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
        charset='utf8mb4',
        cursorclass=DictCursor,
    )


def get_reader_cnx(database='', env_key_prefix='') -> Connection:
    return _get_cnx('READER', database, env_key_prefix)


def get_writer_cnx(database='', env_key_prefix='') -> Connection:
    return _get_cnx('WRITER', database, env_key_prefix)
