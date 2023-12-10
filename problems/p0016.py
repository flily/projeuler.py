#!/usr/bin/env python3
# coding: utf-8


"""
Power Digit Sum

2 ^ 15 = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.

What is the sum of the digits of the number 2 ^ 1000?
"""


PID = 16
ANSWER = 1366


def solve_as_string() -> int:
    n = 2 ** 1000
    s = str(n)
    return sum(int(x) for x in s)


def solve_as_integer() -> int:
    n = 2 ** 1000
    s = 0
    while n > 0:
        s += n % 10
        n //= 10

    return s
