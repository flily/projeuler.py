#!/usr/bin/env python3
# coding: utf-8


"""
Self Powers

The series, 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317.

Find the last ten digits of the series, 1^1 + 2^2 + 3^3 + ... + 1000^1000.
"""


ANSWER = 9110846700


def solve_naive() -> int:
    s = 0
    for i in range(1, 1001):
        s += i**i

    return s % 10**10


def power_mod(n: int, p: int, m: int) -> int:
    """
    Calculate n^p mod m.
    """
    result = 1
    while p > 0:
        result *= n % m
        p -= 1

    return result


def solve_mod_on_power() -> int:
    s = 0
    for i in range(1, 1001):
        s += power_mod(i, i, 10**10)

    return s % 10**10
