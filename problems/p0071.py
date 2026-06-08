#!/usr/bin/env python3
# coding: utf-8


"""
Ordered Fractions

Consider the fraction, n / d, where n and d are positive integers. If n < d and HCF(n, d) = 1,
it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d <= 8 in ascending order of size, we get:
    1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 4/5, 5/6,
    6/7, 7/8

It can be seen that 2/5 is the fraction immediately to the left of 3/7.

By listing the set of reduced proper fractions for d <= 1_000_000 in ascending order of size,
find the numerator of the fraction immediately to the left of 3/7.
"""


ANSWER = 428570

LIMIT = 1_000_000

#  n     p            n * q - d * p
# --- - --- = 0  =>  --------------- = 0
#  d     q                d * q
#
# => n * q - d * p = 0
# => n * q = d * p
# => n = d * p / q

def solve() -> int:
    p, q = 3, 7
    target = p / q
    min_diff = 1.0
    min_n, min_d = 0, 0

    for d in range(3, LIMIT + 1):
        if d % q == 0:
            continue

        n = (d * p) // q
        diff = target - n / d
        if diff < min_diff:
            min_diff = diff
            min_n, min_d = n, d

    del min_d

    return min_n
