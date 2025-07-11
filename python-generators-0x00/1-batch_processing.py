#!/usr/bin/env python3
"""Fetches rows from database in batch and process them"""

import seed

def stream_users_in_batches(batch_size):
    """Fetch rows of users in batch from database.

    :param batch_size: number of rows to fetch from database
    :type batch_size: int
    :yield: the next `batch_size` rows of users
    :rtype: tuple
    """
    conn = seed.connect_to_prodev()
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_data")
    num = batch_size if batch_size > 0 else 0

    if not num:
        return None
    
    while rows := cur.fetchmany(num):
        yield rows
    return None

def batch_processing(batch_size):
    """Process batch of database rows and filter users over the age of 25.

    :param batch_size: number of rows to process
    :type batch_size: int
    """
    try:
        num = batch_size if batch_size > 0 else 0
        keys = ("user_id", "name", "email", "age")
        gen = stream_users_in_batches(num)

        while rows := next(gen):
            for row in rows:
                if row[3] > 25:
                    print(dict(zip(keys, row)))
                    
    except StopIteration:
        return
