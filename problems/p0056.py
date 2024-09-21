#!/usr/bin/env python3
# coding: utf-8


"""
Powerful Digit Sum

A googol (10^100) is a massive number: one followed by one-hundred zeros; 100^100 is almost
unimaginably large: one followed by two-hundred zeros. Despite their size, the sum of the digits in
each number is only 1.

Considering natural numbers of the form, a^b, where a, b < 100, what is the maximum digital sum?
"""


ANSWER = 972


def digit_sum(n: int) -> int:
    """
    Get the sum of the digits of n.
    """
    s = 0
    while n > 0:
        s += n % 10
        n //= 10

    return s


def solve() -> int:
    result = 0
    for a in range(2, 100):
        for b in range(2, 100):
            n = a**b
            s = digit_sum(n)
            result = max(result, s)

    return result
