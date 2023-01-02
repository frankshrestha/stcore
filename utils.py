import json
import boto3

from os import getenv, uname


def _validate_secrets(secret: dict):

    status, message = (True, 'Successfully retrieved secrets.') if all(
        secret.values()) else (False, 'Some secrets are missing.')

    return {
        'status': status,
        'message': message,
        'data': secret
    }


def _get_secrets(endpoint):

    secret_id = getenv('SECRET_ID', '')

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


def _get_env_secrets(endpoint):

    secret = {
        'user': getenv('USERNAME', 'root'),
        'password': getenv('PASSWORD', ''),
        'host': getenv(f'{endpoint}_HOST', 'localhost'),
        'port': int(getenv('PORT', 3306)),
        'database': getenv('DATABASE', '')
    }

    return _validate_secrets(secret)


def _get_cnx_params(endpoint=None, database=None):
    on_cloud = True if ('amzn' in uname().release) else False

    if on_cloud:
        resp = _get_secrets(endpoint)

        if resp['status']:
            return resp['data'].values()

        print(
            f'{resp["message"]}\n{resp["data"]}\nFalling back to environment variables.')

    resp = _get_env_secrets(endpoint)

    if resp['status']:
        return resp['data'].values()

    if on_cloud:
        raise ValueError('Required environment variables missing.')

    resp['data']['database'] = database

    return resp['data'].values()
