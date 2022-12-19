import json
from inspect import cleandoc
from typing import Any, Literal, TypeVar, overload

T = TypeVar('T', bound=dict[str, Any])


@overload
def read_sql(cnx, sql: str) -> list[Any]: ...
@overload
def read_sql(cnx, sql: str, fetch: Literal['all']) -> list[Any]: ...
@overload
def read_sql(cnx, sql: str, fetch: Literal[1, 'one']) -> dict[str, Any]: ...
def read_sql(cnx, sql: str, fetch: Literal[1, 'one', 'all'] = 'all') -> 'dict[str, Any] | list[Any]':
    with cnx.cursor() as cursor:
        cursor.execute(cleandoc(sql))

        if str(fetch) in ['1', 'one']:
            return cursor.fetchone() or {}

        return cursor.fetchall() or []


def write_sql(cnx, sql: str, args: 'dict | list | None' = None):
    sql = cleandoc(sql)

    with cnx.cursor() as cursor:
        if isinstance(args, list):
            cursor.executemany(sql, args)
        else:
            cursor.execute(sql, args)

        cnx.commit()

        return cursor.lastrowid


def key_by(data: list[T], key: str, lowercase_key: bool = False) -> dict[str, T]:
    return {(str(item[key]).lower() if lowercase_key else str(item[key])): item for item in data}


def group_by(data: list[T], key: str, lowercase_key: bool = False) -> dict[str, list[T]]:
    items = {}

    for item in data:
        items.setdefault(
            (str(item[key]).lower() if lowercase_key else str(item[key])),
            [],
        ).append(item)

    return items


def get_tuple(data: list) -> tuple:
    return tuple(data + data if len(data) == 1 else data)


def chunk(data: list, size: int):
    for i in range(0, len(data), size):
        yield data[i : i + size]


def response(data: 'dict[str, Any] | list[Any] | str', status_code: int = 200) -> dict[str, Any]:
    return {
        'statusCode': status_code,
        'body': data if isinstance(data, str) else json.dumps(data),
        'headers': {'content-type': 'application/json'},
    }
