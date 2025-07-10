#!/usr/bin/env python3
"""Connect to a MySQL server, Create a database and a table and insert data to
table from a csv file.
"""
import csv
import mimetypes
import uuid
import MySQLdb
from dotenv import dotenv_values

db = dotenv_values(".env")


def connect_db():
    """Connect to a MySQL database.

    :returns: a connection object to local MySQL database server
    :rtype: MySQLdb.connections.Connection
    """
    return MySQLdb.connect(user=db['user'], password=db['pwd'])


def create_database(connection):
    """Create the database `ALX_prodev` if it does not exist.

    :param connection: a connection object to MySQL database server
    :type connection: MySQLdb.connections.Connection
    """
    if connection and isinstance(connection, MySQLdb.connections.Connection):
        cur = connection.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        cur.close()
        connection.commit()
    else:
        print("Please provide a MySQLdb Connection object.")


def connect_to_prodev():
    """Connect to the `ALX_prodev` MySQL database.

    :returns: a connection object to `ALX_prodev` database
    :rtype: MySQLdb.connections.Connection
    """
    return MySQLdb.connect(user=db['user'],
                           password=db['pwd'],
                           database=db['name'])


def create_table(connection):
    """Create table `user_data` if it does not exist.

    :param connection: a connection object to MySQL database server
    :type connection: MySQLdb Connection
    """
    if connection and isinstance(connection, MySQLdb.connections.Connection):
        cur = connection.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age TINYINT UNSIGNED NOT NULL,
        INDEX (user_id));
        """)
        cur.close()
        connection.commit()
    else:
        print("Please provide a MySQLdb Connection object.")


def insert_data(connection, data):
    """Insert data in the database if it does not exist.

    :param connection: a connection object to MySQL database server
    :type connection: MySQLdb.connections.Connection
    :param data: a CSV file
    :type data: File object
    """
    if connection and isinstance(connection, MySQLdb.connections.Connection):
        cur = connection.cursor()
        cur.execute("SELECT COUNT(*) FROM user_data")
        if cur.fetchone()[0]:
            cur.close()
        else:
            try:
                file_type = mimetypes.guess_type(data)[0]
                if file_type == "text/csv":
                    with open(data) as csv_file:
                        csv_rows = csv.reader(csv_file)
                        next(csv_rows)
                        for row in csv_rows:
                            user_id = str(uuid.uuid4())
                            cur.execute(
                                """INSERT INTO user_data
                                (user_id, name, email, age)
                                VALUES (%s, %s, %s, %s);
                                """, [user_id] + row)
                        connection.commit()
                else:
                    print("Please provide a csv data file.")

            except TypeError:
                print("Please provide a data filename.")
            except FileNotFoundError:
                print("data file cannot be found.")
            finally:
                cur.close()
    else:
        print("Please provide a MySQLdb Connection object.")
