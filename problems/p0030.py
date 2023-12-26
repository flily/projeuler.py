#!/usr/bin/env python3
# coding: utf-8


"""
Digit Fifth Powers

Surprisingly there are only three numbers that can be written as the sum of fourth powers of their
digits:
        1634 = 1^4 + 6^4 + 3^4 + 4^4
        8208 = 8^4 + 2^4 + 0^4 + 8^4
        9474 = 9^4 + 4^4 + 7^4 + 4^4

As 1 = 1^4 is not a sum it is not included.
The sum of these numbers is 1634 + 8208 + 9474 = 19316.

Find the sum of all the numbers that can be written as the sum of fifth powers of their digits.
"""


ANSWER = 443839


def sum_of_digit_power_in_math(n: int, p: int) -> int:
    """
    Get the sum of the pth power of each digit of n.
    """
    result = 0
    while n > 0:
        result += (n % 10) ** p
        n //= 10

    return result


def solve_in_math() -> int:
    result = 0
    n = 2
    max_n = 6 * (9 ** 5)
    while n < max_n:
        if n == sum_of_digit_power_in_math(n, 5):
            result += n
        n += 1

    return result


def sum_of_digit_power_in_string(n: int, p: int) -> int:
    """
    Get the sum of the pth power of each digit of n.
    """
    return sum(int(x) ** p for x in str(n))


def solve_in_string() -> int:
    result = 0
    n = 2
    max_n = 6 * (9 ** 5)
    while n < max_n:
        if n == sum_of_digit_power_in_string(n, 5):
            result += n
        n += 1

    return result
