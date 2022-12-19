from .utils import _get_cnx_params

import pymysql


def _get_cnx(endpoint=None, database=None):

    user, password, host, port, database = _get_cnx_params(endpoint, database)

    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


def get_reader_cnx(database=None):
    return _get_cnx('READER', database)


def get_writer_cnx(database=None):
    return _get_cnx('WRITER', database)
