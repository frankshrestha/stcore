import json
from os import environ, getenv
from platform import uname

import boto3


def _validate_secrets(secret: dict):

    status, message = (True, 'Successfully retrieved secrets.') if all(
        secret.values()) else (False, 'Some secrets are missing.')

    return {
        'status': status,
        'message': message,
        'data': secret
    }


def _get_secrets(endpoint, env_key_prefix):

    secret_id = getenv(f'{env_key_prefix}SECRET_ID', '')

    if not secret_id:
        return {'status': False, 'message': 'SECRET_ID not found in environment.', 'data': {}}

    secret_manager = boto3.client('secretsmanager')

    secret = json.loads(secret_manager.get_secret_value(
        SecretId=secret_id)['SecretString'])

    secret = {
        'user': secret['username'],
        'password': secret['password'],
        'host': secret['host'] if (endpoint == 'WRITER') else secret['hostreader'],
        'port': int(secret['port']),
        'database': secret['database']
    }

    return _validate_secrets(secret)


def _get_env_secrets(endpoint, env_key_prefix):

    host = 'host.docker.internal' if 'LOCALSTACK_HOSTNAME' in environ else 'localhost'

    secret = {
        'user': getenv(f'{env_key_prefix}USERNAME', 'root'),
        'password': getenv(f'{env_key_prefix}PASSWORD', ''),
        'host': getenv(f'{env_key_prefix}{endpoint}_HOST', host),
        'port': int(getenv(f'{env_key_prefix}PORT', 3306)),
        'database': getenv(f'{env_key_prefix}DATABASE', '')
    }

    return _validate_secrets(secret)


def _get_cnx_params(endpoint=None, database='', env_key_prefix=''):

    on_cloud = 'amzn' in uname().release
    env_key_prefix = f'{env_key_prefix}_' if env_key_prefix else ''

    if on_cloud:
        resp = _get_secrets(endpoint, env_key_prefix)

        if resp['status']:
            return resp['data'].values()

        print(
            f'{resp["message"]}\n{resp["data"]}\nFalling back to environment variables.')

    resp = _get_env_secrets(endpoint, env_key_prefix)

    if resp['status']:
        return resp['data'].values()

    if on_cloud:
        raise ValueError('Required environment variables missing.')

    resp['data']['database'] = database

    return resp['data'].values()
