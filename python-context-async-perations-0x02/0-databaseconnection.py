#!/usr/bin/env python3
"""A class based context manager to handle opening and closing database
connections automatically.
"""
import sqlite3


class DatabaseConnection:
    """A class based context manager for database connection.
    """

    def __init__(self, db_name):
        """Constructor
        """
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Create database connection.
        """
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exception_type, exception_value, exception_traceback):
        """Close database connection.
        """
        if exception_type:
            print(f"{exception_type.__name__}: {exception_value}")
            return True
        if self.conn:
            self.conn.close()


def execute_query(query):
    """Execute a database query.
    """
    with DatabaseConnection("users.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        return cur.fetchall()


# Execute a database query
if __name__ == "__main__":
    query = "SELECT * FROM users"
    rows = execute_query(query)

    for row in rows:
        print(row)
