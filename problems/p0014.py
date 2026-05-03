#!/usr/bin/env python3
# coding: utf-8


"""
Longest Collatz Sequence

The following iterative sequence is defined for the set of positive integers:
    n -> n / 2 (n is even)
    n -> 3n + 1 (n is odd)

Using the rule above and starting with 13, we generate the following sequence:
        13 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1

It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms. Although it
has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at 1.

Which starting number, under one million, produces the longest chain?

NOTE: Once the chain starts the terms are allowed to go above one million.
"""


from typing import Iterator


PID = 14
ANSWER = 837799


MAX_NUM = 1_000_000


def collatz_seq(n: int) -> Iterator[int]:
    """
    Generate the Collatz sequence starting at n.
    """
    while n > 1:
        yield n
        if n % 2 == 0:
            n = n / 2
        else:
            n = (3 * n) + 1

    yield 1


def collatz_seq_size(n: int) -> int:
    """
    Get the size of the Collatz sequence starting at n.
    """
    c = 0
    for _ in collatz_seq(n):
        c += 1

    return c


def solve_naive() -> int:
    result, count = 1, 1
    n = 1
    while n < MAX_NUM:
        c = collatz_seq_size(n)
        if c > count:
            result = n
            count = c

        n += 1

    return result


class CollatzCacheMap:
    """
    Cache for Collatz sequences.
    """

    def __init__(self):
        self.cache = {1: 1, 2: 2, 3: 9, 4: 4}
        # for n in range(25):
        #     self.cache[2 ** n] = n + 1

    def calc_length(self, n: int) -> int:
        """
        Get the size of the Collatz sequence starting at n.
        """
        m = n
        result = 1
        while m > 1:
            if m in self.cache:
                result += self.cache[m]
                break

            result += 1
            if m % 2 == 0:
                m = m // 2
            else:
                m = (3 * m) + 1

        self.cache[n] = result
        return result


def solve_with_cache_map() -> int:
    cache = CollatzCacheMap()
    result, count = 1, 1
    n = 1
    while n < MAX_NUM:
        c = cache.calc_length(n)
        if c > count:
            result = n
            count = c

        n += 1

    return result


class CollatzCacheList:
    """
    Cache for Collatz sequences.
    """
    cache: list[int | None]

    def __init__(self, max_size: int):
        self.max_size = max_size
        self.cache = [None] * max_size
        self.cache[0] = 1
        self.cache[1] = 1
        self.cache[2] = 2
        self.cache[3] = 9
        self.cache[4] = 4

    def calc_length(self, n: int) -> int:
        """
        Get the size of the Collatz sequence starting at n.
        """
        m = n
        result = 1
        while m > 1:
            if m < self.max_size and self.cache[m] is not None:
                result += self.cache[m]
                break

            result += 1
            if m % 2 == 0:
                m = m // 2
            else:
                m = (3 * m) + 1

        self.cache[n] = result
        return result


def solve_with_cache_list() -> int:
    cache = CollatzCacheList(MAX_NUM + 1)
    result, count = 1, 1
    n = 1
    while n < MAX_NUM:
        c = cache.calc_length(n)
        if c > count:
            result = n
            count = c

        n += 1

    return result
