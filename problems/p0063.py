#!/usr/bin/env python3
# coding: utf-8


"""
Powerful Digit Counts

The 5-digit number, 16807 = 7 ^ 5, is also a fifth power. Similarly, the 9-digit number,
134217728 = 8 ^ 9, is a ninth power.

How many n-digit positive integers exist which are also an n-th power?
"""


import math


ANSWER = 49


def find_n_power_number(n: int) -> int:
    """
    Find n-digit numbers that are also n-th powers.
    """
    count = 0

    i = 1
    while True:
        num = i ** n
        digits = int(math.log10(num)) + 1
        if digits == n:
            # print(f"found {n}-digit n-th power: {num} = {i} ^ {n}")
            count += 1

        elif digits > n:
            break

        i += 1

    return count

def solve() -> int:
    result = 0
    for i in range(1, 25):
        count = find_n_power_number(i)
        result += count
        if count == 0:
            break

    return result
