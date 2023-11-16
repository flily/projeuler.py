#!/usr/bin/env python3
# coding: utf-8


"""
Sum Square Difference

The sum of the squares of the first ten natural numbers is,
    1^2 + 2^2 + ... + 10^2 = 385

The square of the sum of the first ten natural numbers is,
    (1 + 2 + ... + 10)^2 = 55^2 = 3025

Hence the difference between the sum of the squares of the first ten natural numbers and the square
of the sum is 3025 - 385 = 2640.

Find the difference between the sum of the squares of the first one hundred natural numbers and the
square of the sum.
"""


PID = 6
ANSWER = 25164150


def solve() -> int:
    square_sum = sum([ x * x for x in range(1, 101)])
    sum_square = 5050 * 5050
    return sum_square - square_sum
