#!/usr/bin/env python3
# coding: utf-8


"""
Digit Factorials

145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.

Find the sum of all numbers which are equal to the sum of the factorial of their digits.

Note: As 1! = 1 and 2! = 2 are not sums, they are not included.
"""


from typing import Iterable


ANSWER = 40730


def factorial(n: int) -> int:
    """
    Get the factorial of n.
    """
    if n == 0:
        return 1

    result = n
    for i in range(2, n):
        result *= i

    return result


def is_sum_of_digital_factorials(n: int) -> bool:
    """
    Check if n is equal to the sum of the factorial of its digits.
    """
    s, m = 0, n
    while m > 0:
        s += factorial(m % 10)
        m //= 10

    return s == n


def solve_naive() -> int:
    result = 0
    max_n = factorial(9) + factorial(8)
    for n in range(3, max_n + 1):
        if is_sum_of_digital_factorials(n):
            result += n

    return result


def is_sum_of_digital_factorials_with_table(table: Iterable[int], n: int) -> bool:
    """
    Check if n is equal to the sum of the factorial of its digits.
    """
    s, m = 0, n
    while m > 0:
        s += table[m % 10]
        m //= 10

    return s == n


def solve_with_factorial_table() -> int:
    result = 0
    table = [factorial(i) for i in range(10)]
    max_n = factorial(9) + factorial(8)
    for n in range(3, max_n + 1):
        if is_sum_of_digital_factorials_with_table(table, n):
            result += n

    return result
