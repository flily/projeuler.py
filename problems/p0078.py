#!/usr/bin/env python3
# coding: utf-8


"""
Coin Partitions

Let p(n) represent the number of different ways in which m coins can be separated into piles.
For example, five coins can be separated into piles in exactly seven different ways, so p(5) = 7.

    ◯◯◯◯◯
    ◯◯◯◯ ◯
    ◯◯◯ ◯◯
    ◯◯◯ ◯ ◯
    ◯◯ ◯◯ ◯
    ◯◯ ◯ ◯ ◯
    ◯ ◯ ◯ ◯ ◯

Find the least value of n for which p(n) is divisible by one million.
"""


ANSWER = 55374
TIMEOUT_EXT = {
    "partition_cache_mod": 4000.0,
}

DIVISOR = 1_000_000


def count_sum_cache(cache: dict[tuple[int, int], int], mod: int, target: int, max_num: int) -> int:
    key = (target, max_num)
    if key in cache:
        return cache[key]

    if target == 0:
        return 1

    count = 0
    start = min(target, max_num)
    for x in range(start, 0, -1):
        new_target = target - x
        c = count_sum_cache(cache, mod, new_target, min(x, new_target))
        count = (count + c) % mod

    cache[key] = count
    return count

def solve_cache() -> int:
    """
    use cache (dict)
    """
    cache = {}

    n = 19
    while True:
        p = count_sum_cache(cache, DIVISOR, n, n)
        if p == 0:
            return n

        n += 5


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

# checked, correct. It is too slow when use no cache
# Python 3.14: ~3.5s
# PyPy 7.3 (3.10): ~1.4s
def solve_partition_cache() -> int:
    """
    partitions function (cached)
    """
    cache = {}

    n = 1
    while True:
        p = partitions_cache(cache, n)
        if p % DIVISOR == 0:
            return n

        n += 1


def partitions_cache_mod(cache: dict[int, int], mod: int, n: int) -> int:
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

        result += sign * partitions_cache_mod(cache, mod, n - i)
        result %= mod

        i += x
        if i > n:
            break

        result += sign * partitions_cache_mod(cache, mod, n - i)
        result %= mod

    cache[n] = result
    return result

def solve_partition_cache_mod() -> int:
    """
    partitions function with modulo
    """
    cache = {}

    n = 1
    while True:
        p = partitions_cache_mod(cache, DIVISOR, n)
        if p == 0:
            return n

        n += 1
