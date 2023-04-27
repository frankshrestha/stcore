from .utils import _get_cnx_params

import pymysql


def _get_cnx(endpoint=None, database='', env_key_prefix=''):

    user, password, host, port, database = _get_cnx_params(
        endpoint, database, env_key_prefix)

    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


def get_reader_cnx(database='', env_key_prefix=''):
    return _get_cnx('READER', database, env_key_prefix)


def get_writer_cnx(database='', env_key_prefix=''):
    return _get_cnx('WRITER', database, env_key_prefix)
