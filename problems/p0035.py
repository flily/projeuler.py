#!/usr/bin/env python3
# coding: utf-8


"""
Circular Primes

The number, 197, is called a circular prime because all rotations of the digits: 197, 971, and 719,
are themselves prime.

There are thirteen such primes below 100: 
2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.

How many circular primes are there below one million?
"""


import math
import itertools


ANSWER = 55


def is_prime(n: int) -> bool:
    """
    Check if n (positive) is a prime
    """
    if n <= 2:
        return True

    if n % 2 == 0:
        return False

    i = 3
    while i * i <= n:
        if n % i == 0:
            return False

        i += 2

    return True


def is_circular_prime(n: int) -> bool:
    """
    Check if n is a circular prime
    """
    if not is_prime(n):
        return False

    if n < 10:
        return True

    size = math.floor(math.log10(n)) + 1
    for _ in range(size):
        d = n % 10
        n = (n // 10) + (d * (10 ** (size - 1)))
        if not is_prime(n):
            return False

    return True


def solve_naive() -> int:
    result = 13
    for n in range(101, 1_000_000, 2):
        if is_circular_prime(n):
            result += 1

    return result


def find_circular_prime_with_n_digits(n: int) -> int:
    """
    Find circular primes with n digits
    """
    result = 0
    digits = [range(1, 10, 2)] * n
    for d in itertools.product(*digits):
        m = 0
        for i in range(n):
            m += d[i] * (10 ** (n - i - 1))

        if is_circular_prime(m):
            result += 1

    return result


def solve_with_even_filter() -> int:
    result = 13
    for n in range(3, 7):
        d = find_circular_prime_with_n_digits(n)
        result += d

    return result
