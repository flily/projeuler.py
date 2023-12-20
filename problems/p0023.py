#!/usr/bin/env python3
# coding: utf-8


"""
Non-Abundant Sums

A perfect number is a number for which the sum of its proper divisors is exactly equal to the
number. For example, the sum of the proper divisors of 28 would be 1 + 2 + 4 + 7 + 14 = 28, which
means that 28 is a perfect number.

A number n is called deficient if the sum of its proper divisors is less than n and it is called
abundant if this sum exceeds n.

As 12 is the smallest abundant number, 1 + 2 + 3 + 6 = 16, the smallest number that can be writaten
as the sum of two abundant numbers is 24. By mathematical analysis, it can be shown that all
integers greater than 28123 can be written as the sum of two abundant numbers. However, this upper
limit cannot be reduced any further by analysis even though it is known that the greatest number
that cannot be expressed as the sum of two abundant numbers is less than this limit.

Find the sum of all the positive integers which cannot be written as the sum of two abundant
numbers.
"""

from typing import Mapping


PID = 23
ANSWER = 4179871


LIMIT = 28123


def sum_of_factors(n: int) -> int:
    """
    Get the sum of the factors of n.
    """
    result = 1
    i = 2
    while i * i <= n:
        if n % i == 0:
            result += i
            if i * i != n:
                result += n // i

        i += 1

    return result


def check_type(n: int) -> int:
    """
    Check if n is deficient, perfect, or abundant.
    """
    s = sum_of_factors(n)
    if s < n:
        # Deficient
        return -1

    if s == n:
        # Perfect
        return 0

    # Abundant
    return 1


def solve_naive() -> int:
    result = 0
    n = 1
    while n < LIMIT:
        i = 1
        found = False
        while i < n:
            j = n - i
            if check_type(i) == 1 and check_type(j) == 1:
                found = True
                break

            i += 1

        if not found:
            result += n
        n += 1

    return result


def check_type_with_cache(cache: Mapping[int, int], n: int) -> int:
    """
    Check if n is deficient, perfect, or abundant.
    """
    if n in cache:
        s = cache[n]
    else:
        s = sum_of_factors(n)
        cache[n] = s

    if s < n:
        # Deficient
        return -1

    if s == n:
        # Perfect
        return 0

    # Abundant
    return 1


def solve_with_cache() -> int:
    result = 0
    cache = {}
    n = 1
    while n <= LIMIT:
        i = 1
        found = False
        while i < n:
            j = n - i
            if (
                check_type_with_cache(cache, i) == 1
                and check_type_with_cache(cache, j) == 1
            ):
                found = True
                break

            i += 1

        if not found:
            result += n
        n += 1

    return result


def solve_with_substraction() -> int:
    abundant_numbers = []
    abundant_set = set()

    n = 1
    result = 0
    while n <= LIMIT:
        factor_sum = sum_of_factors(n)
        if factor_sum > n:
            abundant_numbers.append(n)
            abundant_set.add(n)

        is_sum_of_abundant = False
        for x in abundant_numbers:
            if x >= n:
                break

            if n - x in abundant_set:
                is_sum_of_abundant = True
                break

        if not is_sum_of_abundant:
            result += n

        n += 1

    return result
