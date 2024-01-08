#!/usr/bin/env python3
# coding: utf-8


"""
Sub-string Divisibility

The number, 1406357289, is a 0 to 9 pandigital number because it is made up of each of the digits
0 to 9 in some order, but it also has a rather interesting sub-string divisibility property.

Let d1 be the 1st digit, d2 be the 2nd digit, and so on. In this way, we note the following:
        d2 * d3 * d4 = 406 is divisible by 2
        d3 * d4 * d5 = 063 is divisible by 3
        d4 * d5 * d6 = 635 is divisible by 5
        d5 * d6 * d7 = 357 is divisible by 7
        d6 * d7 * d8 = 572 is divisible by 11
        d7 * d8 * d9 = 728 is divisible by 13
        d8 * d9 * d10 = 289 is divisible by 17

Find the sum of all 0 to 9 pandigital numbers with this property.
"""


import itertools


ANSWER = 16695334890


PRIMES = [2, 3, 5, 7, 11, 13, 17]


def solve() -> int:
    result = 0
    for d in itertools.permutations(range(10)):
        if d[0] == 0:
            continue

        found = True
        for i in range(7):
            n = d[i + 1] * 100 + d[i + 2] * 10 + d[i + 3]
            if n % PRIMES[i] != 0:
                found = False
                break

        if found:
            m = 0
            for i in range(10):
                m = m * 10 + d[i]
            result += m

    return result
