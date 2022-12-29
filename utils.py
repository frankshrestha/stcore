from os import getenv, uname


def _get_cnx_params(endpoint=None, database=None):
    on_cloud = True if ('amzn' in uname().release) else False

    database = '' if on_cloud else database

    database = getenv('DATABASE', database)
    if not database:
        raise ValueError(
            'Provide database name or set DATABASE in the environment.')

    host = getenv(f'{endpoint}_HOST', 'localhost')
    port = int(getenv('PORT', 3306))
    user = getenv('USERNAME', 'root')
    password = getenv('PASSWORD', '')

    return user, password, host, port, database
