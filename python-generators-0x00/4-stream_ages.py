#!/usr/bin/env python3
"""A generator that compute average age for a large dataset using
a memory-efficient aggregate function. 
"""
import seed

def stream_user_ages():
    """A generator that yields user ages one by one.

    :yield: age of a user
    :rtype: int
    """
    conn = seed.connect_to_prodev()
    cur = conn.cursor()
    cur.execute("SELECT age FROM user_data")

    while age := cur.fetchone():
        yield age[0]

    return None

def average_user_age():
    """Calculate the average age of users.
    """
    num_users = 0
    sum_ages = 0
    gen = stream_user_ages()

    try:
        while age := next(gen):
            sum_ages += age
            num_users += 1
    except StopIteration:
        print(f"Average age of users: {sum_ages / num_users}")

average_user_age()
