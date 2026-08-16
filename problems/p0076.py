#!/usr/bin/env python3
# coding: utf-8


"""
Counting Summations

It is possible to write five as a sum in exactly six different ways:
    4 + 1
    3 + 2
    3 + 1 + 1
    2 + 2 + 1
    2 + 1 + 1 + 1
    1 + 1 + 1 + 1 + 1

How many different ways can one hundred be written as a sum of at least two positive integers?
"""


import functools


ANSWER = 190569291
TIMEOUT_EXT = {
    "naive": .0,
}

def count_sum(target: int, max_num: int) -> int:
    if target == 0:
        return 1

    count = 0
    start = min(target, max_num)
    for x in range(start, 0, -1):
        count += count_sum(target - x, x)

    return count

# correct solution, but it tasks about 1 minute in pypy.
def solve_naive() -> int:
    target = 100
    result = count_sum(target, target)
    return result - 1


def count_sum_cache(cache: dict[tuple[int, int], int], target: int, max_num: int) -> int:
    key = (target, max_num)
    if key in cache:
        return cache[key]

    if target == 0:
        return 1

    count = 0
    start = min(target, max_num)
    for x in range(start, 0, -1):
        new_target = target - x
        count += count_sum_cache(cache, new_target, x)

    cache[key] = count
    return count


def solve_cache() -> int:
    """
    use cache (dict)
    """
    target = 100
    cache = {}
    result = count_sum_cache(cache, target, target)
    return result - 1


@functools.cache
def count_sum_cache_wrap(target: int, max_num: int) -> int:
    if target == 0:
        return 1

    count = 0
    start = min(target, max_num)
    for x in range(start, 0, -1):
        count += count_sum_cache_wrap(target - x, x)

    return count

def solve_cache_functools() -> int:
    """
    use cache (functools.cache)
    """
    target = 100
    result = count_sum_cache_wrap(target, target)
    return result - 1


def partitions_cache(cache: dict[int, int], n: int) -> int:
    if n in cache:
        return cache[n]

    if n == 0:
        return 1

    result = 0
    for x in range(1, n + 1):
        sign = (x % 2) * 2 - 1
        i = (3 * x * x - x) // 2
        if i > n:
            break

        result += sign * partitions_cache(cache, n - i)
        i += x
        if i > n:
            break

        result += sign * partitions_cache(cache, n - i)

    cache[n] = result
    return result


def solve_partition() -> int:
    """
    use partitions function
    """
    cache = {}
    n = 100
    return partitions_cache(cache, n) - 1
