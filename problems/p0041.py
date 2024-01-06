#!/usr/bin/env python3
# coding: utf-8


"""
Pandigital Prime

We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly
once. For example, 2143 is a 4-digit pandigital and is also prime.

What is the largest n-digit pandigital prime that exists?
"""


import math
import itertools


ANSWER = 7652413


def is_pandigit(n: int) -> bool:
    """
    Check if n is pandigital.
    """
    digits = [False] * 10
    size = math.floor(math.log10(n)) + 1

    while n > 0:
        d = n % 10
        if d == 0 or digits[d]:
            return False

        digits[d] = True
        n //= 10

    for i in range(1, size):
        if not digits[i]:
            return False

    return True


def is_prime(n: int) -> bool:
    """
    Check if n (positive) is a prime
    """
    if n % 2 == 0:
        return False

    i = 3
    while i * i <= n:
        if n % i == 0:
            return False

        i += 2

    return True


def solve_naive() -> int:
    i = 987654321
    while i > 0:
        if is_pandigit(i) and is_prime(i):
            return i

        i -= 2

    return 0


def solve_by_permutations() -> int:
    size = 9
    while size > 0:
        digits = list(range(1, size + 1))
        digits.sort(reverse=True)
        for p in itertools.permutations(digits):
            n = 0
            for d in p:
                n = n * 10 + d

            if is_prime(n):
                return n

        size -= 1

    return 0
