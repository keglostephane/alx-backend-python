#!/usr/bin/env python3
"""A generator that fetch rows one by one from `user_data` table.
"""

import seed

def stream_users():
    """Fetch rows one by one from `user_data` table.

    :returns: a generator of tuples (rows)
    """
    conn = seed.connect_to_prodev()
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_data")

    while row := cur.fetchone():
        yield row
        
