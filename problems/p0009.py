#!/usr/bin/env python3
# coding: utf-8


"""
Special Pythagorean Triplet

A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,
    a ^ 2 + b ^ 2 = c ^ 2

For example, 3 ^ 2 + 4 ^ 2 = 9 + 16 = 25 = 5 ^ 2.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc.
"""


PID = 9
ANSWER = 31875000


def solve() -> int:
    for a in range(1, 1000):
        for b in range(a + 1, 1000):
            c = 1000 - a - b
            if a * a + b * b == c * c:
                return a * b * c

    return None
