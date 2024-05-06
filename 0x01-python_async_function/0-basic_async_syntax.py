#!/usr/bin/env python3
""" basic_async_syntax Module
"""
import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    """"Wait for a random delay and return that delay."""
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
