#!/usr/bin/env python3
# coding: utf-8


"""
Amicable Numbers

Let d(n) be defined as the sum of proper divisors of n (numbers less than n which divide evenly
into n).
If d(a) = b and d(b) = a, where a ≠ b, then a and b are an amicable pair and each of a and b are
called amicable numbers.

For example, the proper divisors of 220 are 1, 2, 4, 5, 10, 11, 20, 22, 44, 55 and 110; therefore
d(220) = 284. The proper divisors of 284 are 1, 2, 4, 71 and 142; so d(284) = 220.

Evaluate the sum of all the amicable numbers under 10000.
"""


PID = 21
ANSWER = 31626


LIMIT = 10000


def find_divisors(n: int) -> list:
    """
    Find all the divisors of n.
    """
    result = [1]
    for i in range(2, n):
        if n % i == 0:
            result.append(i)

    return result


def solve_naive() -> int:
    result = 0
    divisor_sums = {}
    n = 1
    while n < LIMIT:
        divisors = find_divisors(n)
        s = sum(divisors)
        divisor_sums[n] = s
        if s != n and s in divisor_sums and divisor_sums[s] == n:
            result += n + s

        n += 1

    return result


def find_divisors_by_sqrt(n: int) -> list:
    """
    Find all the divisors of n.
    """
    result = [1]
    i = 2
    while i * i <= n:
        if n % i == 0:
            result.append(i)
            result.append(n // i)
        i += 1

    return result


def solve_sqrt_finder() -> int:
    result = 0
    divisor_sums = {}
    n = 1
    while n < LIMIT:
        divisors = find_divisors_by_sqrt(n)
        s = sum(divisors)
        divisor_sums[n] = s
        if s != n and s in divisor_sums and divisor_sums[s] == n:
            result += n + s

        n += 1

    return result


def divisors_sum_by_sqrt(n: int):
    """
    Find all the divisors of n.
    """
    result = 1
    i = 2
    while i * i <= n:
        if n % i == 0:
            result += i + (n // i)
        i += 1

    return result


def solve_sqrt_finder_no_array() -> int:
    result = 0
    divisor_sums = {}
    n = 1
    while n < LIMIT:
        s = divisors_sum_by_sqrt(n)
        divisor_sums[n] = s
        if s != n and s in divisor_sums and divisor_sums[s] == n:
            result += n + s

        n += 1

    return result
