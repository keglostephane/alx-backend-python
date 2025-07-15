#!/usr/bin/env python3
"""Run multiple database queries concurently.
"""
import asyncio
import aiosqlite


async def fetch_users():
    """Fetch all users from database.
    """
    query = "SELECT * FROM users"
    async with aiosqlite.connect("users.db") as conn:
        async with conn.execute(query) as cur:
            return await cur.fetchall()


async def fetch_older_users():
    """Fetch users older than 40 from database.
    """
    query = "SELECT * FROM users WHERE age > 40"
    async with aiosqlite.connect("users.db") as conn:
        async with conn.execute(query) as cur:
            return await cur.fetchall()


async def fetch_concurrently():
    """Fetch multiple database queries results concurrently.
    """
    tasks = fetch_users(), fetch_older_users()
    rows = await asyncio.gather(*tasks)

    print(f"Fetch all users: {rows[0]}")
    print(f"Fetch users older than 40: {rows[1]}")


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
