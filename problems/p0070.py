#!/usr/bin/env python3
# coding: utf-8


"""
Totient Permutation

Euler's totient function, Φ(n) [sometimes called the phi function], is used to determine the number
of positive numbers less than or equal to n which are relatively prime to n.For example,
as 1, 2, 4, 5, 7, and 8 are all less than nine and relatively prime to nine, Φ(9) = 6.

The number 1 is considered to be relatively prime to every positive number, so Φ(1) = 1.

Interestingly, Φ(87109) = 79180, and it can be seen that 87109 is a permutation of 79180.

Find the value of n, 1 < n < 10^7, for which Φ(n) is a permutation of n and the ratio n/Φ(n)
produces a minimum.
"""


import math


ANSWER = 303963552391

LIMIT = 1_000_000


def phi(n: int) -> int:
    count = 0
    for i in range(1, n):
        if math.gcd(i, n) == 1:
            count += 1

    return count


def solve_naive() -> int:
    count = 0
    for n in range(2, LIMIT):
        count += phi(n)

    return count


def sieve_phi(max_num: int) -> int:
    """
    Get the value of Φ(n) for n using sieve.
    """
    sieve = [0] * (max_num + 1)

    for i in range(2, max_num + 1):
        if sieve[i] == 0:
            for j in range(i, max_num + 1, i):
                if sieve[j] == 0:
                    sieve[j] = j * (i - 1) // i
                else:
                    sieve[j] = sieve[j] * (i - 1) // i

    return sieve


def solve_sieve() -> int:
    sieve = sieve_phi(LIMIT)
    return sum(sieve)
