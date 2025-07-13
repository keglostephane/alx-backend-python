#!/usr/bin/env python3
"""Handle database connections with a decorator.
"""
import sqlite3 
import functools

def with_db_connection(func):
    """Open a database connection, pass it to function and close it afterword.
    """
    
    functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn=conn, **kwargs)
        finally:
            conn.close()

    return wrapper
        

@with_db_connection 
def get_user_by_id(conn, user_id):
    """Get a user from database using his id.

    :param conn: connection to users database
    :type conn: sqlite3.Connection
    :param user_id: user id
    :type user_id: int
    :returns: the user whose id is `user_id`
    :rtype: tuple
    """
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone()

#### Fetch user by ID with automatic connection handling 
user = get_user_by_id(user_id=1)
print(user)
