#!/usr/bin/env python3
"""A decorator that logs database queries executed by any function.
"""
import sqlite3
import functools

#### decorator to lof SQL queries


def log_queries(func):
    """Log database queries"""
    from datetime import datetime

    functools.wraps(func)
    def wrapper(**kargs):
        print(f"{datetime.now().isoformat()} - Running: {kargs}")
        return func(**kargs)

    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
