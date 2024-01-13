#!/usr/bin/env python3
# coding: utf-8


"""
Distinct Primes Factors

The first two consecutive numbers to have two distinct prime factors are:
            14 = 2 × 7
            15 = 3 × 5

The first three consecutive numbers to have three distinct prime factors are:
            644 = 2^2 × 7 × 23
            645 = 3 × 5 × 43
            646 = 2 × 17 × 19

Find the first four consecutive integers to have four distinct prime factors each. What is the
first of these numbers?
"""


ANSWER = 134043


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


def find_prime_factors(n: int) -> set[int]:
    """
    Find the prime factors of n.
    """
    result = set()
    if n % 2 == 0:
        result.add(2)

    i = 3
    while i * i <= n:
        if n % i == 0:
            if is_prime(i):
                result.add(i)
            if is_prime(n // i):
                result.add(n // i)

        i += 2

    return result

def solve_naive() -> int:
    n = 647
    c = 0

    while True:
        pfs = find_prime_factors(n)
        if len(pfs) == 4:
            c += 1
        else:
            c = 0

        if c == 4:
            break

        n += 1

    return n - 3
