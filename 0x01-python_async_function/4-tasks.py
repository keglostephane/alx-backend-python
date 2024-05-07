#!/usr/bin/env python3
"""4-tasks.py"""
import asyncio
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """run asyncio task n times with the specified delay"""
    tasks = []
    delays = []

    for _ in range(n):
        tasks.append(task_wait_random(max_delay))
    for task in asyncio.as_completed(tasks):
        delays.append(await task)

    return delays
