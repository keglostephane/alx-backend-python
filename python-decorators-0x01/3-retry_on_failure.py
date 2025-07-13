#!/usr/bin/env python3
"""Retry database queries using a decorator.
"""

import time
import sqlite3
import functools


def with_db_connection(func):
    """Open a database connection, pass it to function and close it afterword.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn=conn, **kwargs)
        finally:
            conn.close()

    return wrapper


def retry_on_failure(retries=3, delay=2):
    """Retries the function a number of time if it raises an exception.

    :param retries: number of time to retrieve the function
    :type retries: int
    :param delay: delay (seconds) to wait before another retry
    :type delay: int
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except sqlite3.DatabaseError:
                while retries := kwargs.get('retries'):
                    try:
                        return func(*args, **kwargs)
                        break
                    except sqlite3.DatabaseError:
                        time.sleep(delay)
                    retries -= 1

        return wrapper

    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=180)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


#### attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)
