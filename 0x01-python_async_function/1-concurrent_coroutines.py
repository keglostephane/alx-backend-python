#!/usr/bin/env python3
"""concurrent_coroutines Module"""
import asyncio
from typing import List


wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """Spawn a process n times with the specified delay.

    :param n: number of times to spawn the process
    :param max_delay: max delay for each spawned process to finish
    """
    tasks = []
    delays = []

    for _ in range(n):
        tasks.append(asyncio.create_task(wait_random(max_delay)))
    for task in asyncio.as_completed(tasks):
        delays.append(await task)

    return delays
