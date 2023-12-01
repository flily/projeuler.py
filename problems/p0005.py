#!/usr/bin/env python3
# coding: utf-8


"""
Smallest Multiple

2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any
remainder.

What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?
"""


PID = 5
ANSWER = 232792560


def solve() -> int:
    primes = [2, 3, 5, 7, 11, 13, 17, 19]
    result = 1

    for p in primes:
        for x in range(1, 6):
            if p**x > 20:
                result *= p ** (x - 1)
                break

    return result
