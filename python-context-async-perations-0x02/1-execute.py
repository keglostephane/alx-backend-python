#!/usr/bin/env python3
"""A reusable context manager that takes a query as input, executes it,
managing both connection and the query execution.
"""
import sqlite3

class ExecuteQuery:
    """Take a query as input, execute it, managing both connection
    and the query execution.

    :param query: query to execute
    :type query: str
    :param param: query's parameter
    :type param: int, float, str
    """

    def __init__(self, db_name, query, param):
        """Constructor"""
        self.db_name = db_name
        self.query = query
        self.param = param
        self.conn = None

    def __enter__(self):
        """Create database connection and execute a query.
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()

        if self.query.endswith('?'):
            self.cur.execute(self.query, (self.param,))
        else:
            self.cur.execute(self.query)
    
        return self.cur.fetchall()
        
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        """Close database connection.
        """
        if exception_type:
            print(f"{exception_type.__name__}: {exception_value}")
            return True
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    db_name = "users.db"
    query = "SELECT * FROM users WHERE age > ?"
    param = 25

    with ExecuteQuery(db_name, query, param) as users:
        for user in users:
            print(user)
