#!/usr/bin/env python3
"""Manage database transactions by automatically committing or
rolling back changes.
"""
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


def transactional(func):
    """Run a database operation in a transaction.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = kwargs.get('conn')
        try:
            conn.execute("BEGIN TRANSACTION;")
            func(*args, **kwargs)
        except sqlite3.Error:
            conn.execute("ROLLBACK;")
        else:
            conn.execute("COMMIT;")

    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?",
                   (new_email, user_id))


#### Update user's email with automatic transaction handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
