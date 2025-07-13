#!/usr/bin/env python3
"""Cache the results of database queries in order to avoid redundant calls.
"""
import time
import sqlite3
import functools

query_cache = {}


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


def cache_query(func):
    """Cache query results based on the SQL query string.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query")
        cached = query_cache.get(query)
        start_time = time.perf_counter()
        
        print(f"Executing query: {query}")
        
        if cached:
            print(f"Using cached result for query: {query}")
            return cached
        else:
            result = func(*args, **kwargs)
            query_cache[query] = result

        end_time = time.perf_counter()
        duration = (end_time - start_time) * 1000
        print(f"Execution time: {duration:.3f} ms")

        return result

    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetch users from database or get users from cache.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
