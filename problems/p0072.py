#!/usr/bin/env python3
# coding: utf-8


"""
Counting Fractions

Consider the fraction, n / d, where n and d are positive integers. If n < d and HCF(n, d) = 1,
it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d ≤ 8 in ascending order of size, we get:

    1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 4/5, 5/6,
    6/7, 7/8

It can be seen that there are 21 elements in this set.

How many elements would be contained in the set of reduced proper fractions for d ≤ 1,000,000?
"""

import math


ANSWER = 303963552391

LIMIT = 1_000_000

def solve_naive() -> int:
    count = 0
    for d in range(2, LIMIT + 1):
        for n in range(1, d):
            if math.gcd(n, d) == 1:
                count += 1

    return count


def sieve_totient(max_num: int) -> int:
    """
    Get the value of Φ(n) for n using sieve.
    """
    sieve = [0] * (max_num + 1)
    result = 0

    for i in range(2, max_num + 1):
        if sieve[i] == 0:
            for j in range(i, max_num + 1, i):
                if sieve[j] == 0:
                    sieve[j] = j
                sieve[j] /= i / (i - 1)

        result += sieve[i]

    return result


def solve_sieve() -> int:
    return sieve_totient(LIMIT)
