"""Use rollback journals for the controller's cross-database transactions."""

import sqlite3


_connect = sqlite3.connect


class _ConnectionProxy:
    """Delegate sqlite operations while forcing rollback-journal mode."""

    def __init__(self, connection):
        object.__setattr__(self, "_connection", connection)

    def execute(self, sql, *parameters):
        if "journal_mode" in sql.lower() and "wal" in sql.lower():
            sql = sql.replace("WAL", "DELETE").replace("wal", "DELETE")
        return self._connection.execute(sql, *parameters)

    def __getattr__(self, name):
        return getattr(self._connection, name)

    def __setattr__(self, name, value):
        setattr(self._connection, name, value)


def connect(*args, **kwargs):
    connection = _connect(*args, **kwargs)
    connection.execute("PRAGMA journal_mode = DELETE;")
    return _ConnectionProxy(connection)


sqlite3.connect = connect
