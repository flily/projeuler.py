#!/usr/bin/env python3
# coding: utf-8


"""
Square Digit Chains

A number chain is created by continuously adding the square of the digits in a number to form a new
number until it has been seen before.

For example,
    44 -> 32 -> 13 -> 10 -> [1] -> [1]
    85 -> [89] -> 145 -> 42 -> 20 -> 4 -> 16 -> 37 -> 58 -> [89]

Therefore any chain that arrives at 1 or 89 will become stuck in an endless loop. What is most
amazing is that EVERY starting number will eventually arrive at 1 or 89.

How many starting numbers below ten million will arrive at 89?
"""


ANSWER = 8581146
TIMEOUT_EXT = {
    "reduced_cache_list": 5000.0,
}

LIMIT = 10_000_000


def digit_square_sum(n: int) -> int:
    """
    Get the sum of the squares of the digits of n.
    """
    s = 0
    while n > 0:
        d = n % 10
        s += d * d
        n //= 10

    return s


def check_chains(n: int) -> int:
    """
    Check the chain for n.
    """
    m = n
    p = [m]
    while m not in (1, 89):
        m = digit_square_sum(m)
        p.append(m)

    return m


def solve_naive() -> int:
    result = 0
    n = 1
    while n < LIMIT:
        if check_chains(n) == 89:
            result += 1

        n += 1

    return result


def check_chains_set(n: int, set1: set[int], set89: set[int]) -> int:
    """
    Check the chain for n.
    """
    m = n
    while m not in set1 and m not in set89:
        m = digit_square_sum(m)

    result = 1
    if m in set89:
        result = 89
        set89.add(n)
    else:
        set1.add(n)

    return result


def solve_cache_set() -> int:
    result = 0
    n = 1
    set1 = set([1])
    set89 = set([89])
    while n < LIMIT:
        if check_chains_set(n, set1, set89) == 89:
            result += 1

        n += 1

    return result


def check_chains_reduced_set(n: int, set1: list[bool], set89: list[bool]) -> int:
    m = n
    ok1, ok89 = False, False
    while not ok1 and not ok89:
        m = digit_square_sum(m)
        ok1, ok89 = set1[m], set89[m]

    if n < len(set1):
        if ok89:
            set89[n] = True
        else:
            set1[n] = True

    return 89 if ok89 else 1


def solve_reduced_cache_set() -> int:
    result = 0
    n = 1
    set1 = [None] * (7 * 81 + 1)
    set89 = [None] * (7 * 81 + 1)
    set1[1] = True
    set89[89] = True

    while n < LIMIT:
        if check_chains_reduced_set(n, set1, set89) == 89:
            result += 1

        n += 1

    return result


def solve_reduced_cache_list() -> int:
    result = 0
    size = 7 * 81 + 1
    cache89 = [None] * size

    for n in range(1, size):
        if check_chains(n) == 89:
            cache89[n] = True
            result += 1

    for n in range(size, LIMIT):
        ds = digit_square_sum(n)
        if cache89[ds]:
            result += 1

    return result
