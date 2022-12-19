from os import getenv, uname


def _get_cnx_params(endpoint=None, database=None):
    on_cloud = True if ('amzn' in uname().release) else False

    database = '' if on_cloud else database

    database = getenv(f'{endpoint}_DATABASE', database)
    if not database:
        raise ValueError(
            f"Provide database name or set {endpoint}_DATABASE in the environment.")

    host = getenv(f'{endpoint}_HOST', 'localhost')
    port = getenv(f'{endpoint}_PORT', 3306)
    user = getenv(f'{endpoint}_USERNAME', 'root')
    password = getenv(f'{endpoint}_PASSWORD', '')

    return user, password, host, port, database
