#!/usr/bin/env python3
# coding: utf-8


"""
Prime Permutations

The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330, is unusual
in two ways: (i) each of the three terms are prime, and, (ii) each of the 4-digit numbers are
permutations of one another.

There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this
property, but there is one other 4-digit increasing sequence.

What 12-digit number do you form by concatenating the three terms in this sequence?
"""


import itertools
from typing import Iterable


ANSWER = 296962999629


KNOWN_ANSWER = 1487


def is_prime(n: int) -> bool:
    """
    Check if n (n >= 3) is prime.
    """
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False

        i += 2

    return True


def get_digits(n: int) -> Iterable[int]:
    """
    Get the digits of n.
    """
    while n > 0:
        yield n % 10
        n //= 10


def solve_naive() -> int:
    n = 1001
    while n < 10000:
        if not is_prime(n):
            n += 2
            continue

        pp = set()
        for digit in itertools.permutations(get_digits(n)):
            if digit[0] == 0 or digit[3] % 2 == 0:
                continue

            m = digit[0] * 1000 + digit[1] * 100 + digit[2] * 10 + digit[3]
            if is_prime(m):
                pp.add(m)

        if len(pp) < 3:
            n += 2
            continue

        pl = list(pp)
        pl.sort()
        for i, j, k in itertools.combinations(range(len(pl)), 3):
            if pl[j] - pl[i] == pl[k] - pl[j]:
                if pl[i] != KNOWN_ANSWER:
                    result = pl[i] * 10**8 + pl[j] * 10**4 + pl[k]
                    return result

        n += 2

    return 0
