#!/usr/bin/env python3
# coding: utf-8


"""
Quadratic Primes

Euler discovered the remarkable quadratic formula:
        n ^ 2 + n + 41

It turns out that the formula will produce 40 primes for the consecutive integer values
0 <= n <= 39. However, when n = 40, 40 ^ 2 + 40 + 41 = 40 * (40 + 1) + 41 is divisible by 41, and
certainly when n = 41, 41 ^ 2 + 41 + 41 is clearly divisible by 41.

The incredible formula n ^ 2 - 79 * n + 1601 was discovered, which produces 80 primes for the
consecutive values 0 <= n <= 79. The product of the coefficients, -79 and 1601, is -126479.

Considering quadratics of the form:
        n ^ 2 + a * n + b, where |a| < 1000 and |b| <= 1000

        where |n| is the modulus/absolute value of n
        e.g. |11| = 11 and |-4| = 4

Find the product of the coefficients, a and b, for the quadratic expression that produces the
maximum number of primes for consecutive values of n, starting with n = 0.
"""


from typing import Mapping


ANSWER = -59231


def is_prime(n: int) -> bool:
    """
    Check if n (positive) is a prime
    """
    if n < 2:
        return False

    if n == 2:
        return True

    i = 3
    while i * i <= n:
        if n % i == 0:
            return False

        i += 2

    return True


def f(a: int, b: int, n: int) -> int:
    """
    Get n ^ 2 + a * n + b
    """
    return n * n + a * n + b


def consecutive_prime_size(a: int, b: int) -> int:
    """
    Get the consecutive prime size of n ^ 2 + a * n + b
    """
    x = 0
    while True:
        n = f(a, b, x)
        if not is_prime(n):
            break

        x += 1

    return x


def solve_naive() -> int:
    max_prime_size = 0
    max_a, max_b = 0, 0

    for a in range(-999, 1000):
        for b in range(-1000, 1001):
            s = consecutive_prime_size(a, b)
            if s > max_prime_size:
                max_prime_size = s
                max_a, max_b = a, b

    return max_a * max_b


def is_prime_with_cache(cache: Mapping[int, bool], n: int) -> bool:
    """
    Check if n (positive) is a prime
    """
    if n < 2:
        return False

    if n == 2:
        return True

    if n in cache:
        return cache[n]

    i = 3
    while i * i <= n:
        if n % i == 0:
            cache[n] = False
            return False

        i += 2

    cache[n] = True
    return True


def consecutive_prime_size_with_cache(cache: Mapping[int, bool], a: int, b: int) -> int:
    """
    Get the consecutive prime size of n ^ 2 + a * n + b
    """
    x = 0
    while True:
        n = f(a, b, x)
        if not is_prime_with_cache(cache, n):
            break

        x += 1

    return x


def solve_with_cache() -> int:
    max_prime_size = 0
    max_a, max_b = 0, 0
    cache: Mapping[int, bool] = {}

    for a in range(-999, 1000):
        for b in range(-1000, 1001):
            if (b != 0 and a % b == 0) or (a != 0 and b % a == 0):
                continue

            s = consecutive_prime_size_with_cache(cache, a, b)
            if s > max_prime_size:
                max_prime_size = s
                max_a, max_b = a, b

    return max_a * max_b
