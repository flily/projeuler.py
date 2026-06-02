#!/usr/bin/env python3
# coding: utf-8


"""
Permuted Multiples

It can be seen that the number, 125874, and its double, 251748, contain exactly the same digits,
but in a different order.

Find the smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x, contain the same digits.
"""


ANSWER = 142857


def get_digits(n: int) -> set[int]:
    """
    Get the digits of n.
    """
    result = set()
    while n > 0:
        result.add(n % 10)
        n //= 10

    return result


def solve_digit_set() -> int:
    """
    use digits set
    """
    n = 2
    found = False
    while not found:
        n_digits = get_digits(n)
        same_digits = True
        for x in range(2, 7):
            if get_digits(n * x) != n_digits:
                same_digits = False
                break

        if same_digits:
            found = True
            break

        n += 1

    return n


def get_digits_table(n: int) -> list[int]:
    """
    Get the digits table of n.
    """
    result = [0] * 10
    while n > 0:
        result[n % 10] += 1
        n //= 10

    return result


def solve_table() -> int:
    """
    use digits table
    """
    n = 2
    found = False
    while not found:
        n_digits = get_digits_table(n)
        same_digits = True
        for x in range(2, 7):
            if get_digits_table(n * x) != n_digits:
                same_digits = False
                break

        if same_digits:
            found = True
            break

        n += 1

    return n
