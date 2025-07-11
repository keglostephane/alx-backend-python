#!/usr/bin/env python3
"""Fetch paginated data from `user_data` table using a generator
to lazy load each page.
"""
import seed

def paginate_users(page_size, offset):
    """Fetch paginated data from users database.

    :param pagesize: number of rows per page
    :type pagesize: int
    :param offset: offset to start from
    :type offset: int
    :returns: paginated rows of users
    :rtype: tuple
    """
    from MySQLdb.cursors import DictCursor
    
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(DictCursor)
    cursor.execute(
        f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_paginate(pagesize):
    """Fetch paginated data from users database using a generator
    to lazy load each page.

    :param pagesize: number of rows per page
    :type pagesize: int
    :yield: the next page of users
    :rtype: tuple
    """
    num = pagesize if pagesize > 0 else 0
    offset = 0

    while page := paginate_users(num, offset):
        offset += num
        yield page

    return ()
