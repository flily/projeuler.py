#!/usr/bin/env python3
# coding: utf-8


"""
Champernowne's Constant

An irrational decimal fraction is created by concatenating the positive integers:
        0.12345678910[1]112131415161718192021...

It can be seen that the 12th digit of the fractional part is 1.

If d(n) represents the nth digit of the fractional part, find the value of the following
expression.
        d(1) × d(10) × d(100) × d(1000) × d(10000) × d(100000) × d(1000000)
"""


ANSWER = 210


def d(n: int) -> int:
    """
    Return the nth digit of the fractional part.
    """
    if n < 10:
        return n

    m = n - 9
    i = 2
    num = 10
    while m > 0:
        size = (10**i) - (10 ** (i - 1))
        if m > size * i:
            m -= size * i
            num = 10**i
            i += 1
            continue

        offset = (m - 1) // i
        position = (m - 1) % i
        number = num + offset
        digit = number // (10 ** (i - position - 1)) % 10
        return digit

    return 0


def solve() -> int:
    result = 1
    indexes = [1, 10, 100, 1000, 10000, 100000, 1000000]
    for x in indexes:
        y = d(x)
        result *= y

    return result
