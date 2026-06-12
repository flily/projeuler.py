#!/usr/bin/env python3
# coding: utf-8


"""
Counting Fractions in a Range

Consider the fraction, n / d, where n and d are positive integers. If n < d and HCF(n, d) = 1,
it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d <= 8 in ascending order of size, we get:
    1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 4/5, 5/6,
    6/7, 7/8

It can be seen that there are 3 fractions between 1/3 and 1/2.

How many fractions lie between 1/3 and 1/2 in the sorted set of reduced proper fractions
for d <= 12_000?
"""


import math


ANSWER = 7295372
TIMEOUT_EXT = {
    "math_gcd": 500.0,
    "gcd": 500.0,
}

LIMIT = 12_000


def solve_math_gcd() -> int:
    count = 0
    for d in range(4, LIMIT + 1):
        lower = d // 3 + 1
        upper = (d + 1) // 2

        for n in range(lower, upper):
            if math.gcd(n, d) == 1:
                count += 1

    return count


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b

    return a


def solve_gcd() -> int:
    count = 0
    for d in range(4, LIMIT + 1):
        lower = d // 3 + 1
        upper = (d + 1) // 2

        for n in range(lower, upper):
            if gcd(n, d) == 1:
                count += 1

    return count
