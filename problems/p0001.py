# /usr/bin/env python3
# coding: utf-8


"""
Multiples of 3 and 5

If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The
sum of these multiples is 23.

Find the sum of all the multiples of 3 or 5 below 1000.
"""


PID = 1
ANSWER = 233168


def solve() -> int:
    i = 3
    s = 0
    while i < 1000:
        if i % 3 == 0 or i % 5 == 0:
            s += i

        i += 1

    return s
