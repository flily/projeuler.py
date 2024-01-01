#!/usr/bin/env python3
# coding: utf-8


"""
Truncatable Primes

The number 3797 has an interesting property. Being prime itself, it is possible to continuously
remove digits from left to right, and remain prime at each stage: 3797, 797, 97, and 7. Similarly
we can work from right to left: 3797, 379, 37, and 3.

Find the sum of the only eleven primes that are both truncatable from left to right and right to
left.

NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.
"""


from typing import Iterator
import itertools
import math


ANSWER = 748317


def is_prime(n: int) -> bool:
    """
    Check if n (positive) is a prime
    """
    if n <= 1:
        return False

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    i = 3
    while i * i <= n:
        if n % i == 0:
            return False

        i += 2

    return True


def _is_truncatable_prime_left(n: int) -> bool:
    while n > 0:
        if not is_prime(n):
            return False

        size = math.floor(math.log10(n)) + 1
        n = n % (10 ** (size - 1))

    return True


def _is_truncatable_prime_right(n: int) -> bool:
    while n > 0:
        if not is_prime(n):
            return False

        n = n // 10

    return True


def is_truncatable_prime(n: int) -> bool:
    """
    Check if n is a truncatable prime
    """
    return _is_truncatable_prime_left(n) and _is_truncatable_prime_right(n)


def solve_naive() -> int:
    result = 0
    for i in range(10, 1_000_000):
        if is_truncatable_prime(i):
            result += i

    return result


def truncatable_generator(size: int) -> Iterator[int]:
    """
    Generate all truncatable primes of size
    """
    if size <= 0:
        return

    if size == 1:
        for x in [2, 3, 5, 7]:
            yield x

    digits = [[1, 3, 7, 9]] * size
    digits[size - 1] = [3, 7]
    digits[0] = [2, 3, 5, 7]
    for x in itertools.product(*digits):
        n = 0
        for i in range(size):
            n += x[i] * (10 ** (size - i - 1))

        yield n


def solve_by_generator() -> int:
    result = 0
    for size in range(2, 7):
        for n in truncatable_generator(size):
            if is_truncatable_prime(n):
                result += n

    return result
