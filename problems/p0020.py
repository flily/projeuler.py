#!/usr/bin/env python3
# coding: utf-8


"""
Factorial Digit Sum

n! means n × (n − 1) × ... × 3 × 2 × 1.

For example, 10! = 10 × 9 × ... × 3 × 2 × 1 = 3628800, and the sum of the digits in the number 10!
is 3 + 6 + 2 + 8 + 8 + 0 + 0 = 27.

Find the sum of the digits in 100!.
"""


PID = 20
ANSWER = 648


def factorial(n: int) -> int:
    """
    Get the factorial of n.
    """
    result = n
    for i in range(2, n):
        result *= i

    return result


def solve_in_math() -> int:
    n = factorial(100)
    result = 0
    while n > 0:
        result += n % 10
        n //= 10

    return result


def solve_in_string() -> int:
    n = factorial(100)
    result = 0
    for x in str(n):
        result += int(x)

    return result
