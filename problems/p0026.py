#!/usr/bin/env python3
# coding: utf-8


"""
Reciprocal Cycles

A unit fraction contains 1 in the numerator. The decimal representation of the unit fractions with
denominators 2 to 10 are given:
            
        1/2  = 0.5
        1/3  = 0.(3)
        1/4  = 0.25
        1/5  = 0.2
        1/6  = 0.1(6)
        1/7  = 0.(142857)
        1/8  = 0.125
        1/9  = 0.(1)
        1/10 = 0.1

Where 0.1(6) means 0.166666..., and has a 1-digit recurring cycle. It can be seen that 1/7 has a
6-digit recurring cycle.

Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal
fraction part.
"""


import math


PID = 26
ANSWER = 983


def get_cycle_length(n: int) -> int:
    """
    Get the length of the recurring cycle of 1/n.
    """
    base = 10 ** int(math.ceil(math.log10(n)))
    m = base
    digits = []
    loop_start = -1
    while m != 0:
        r = m // n
        d = m % n
        if d == 0:
            break

        key = (r, d)
        if key in digits:
            loop_start = digits.index(key)
            break

        digits.append(key)
        m = d
        while m < n:
            m *= 10

    if loop_start < 0:
        return 0

    return len(digits) - loop_start


def solve_naive() -> int:
    max_cycle_length = 0
    max_cycle_number = 0
    for i in range(2, 1000):
        l = get_cycle_length(i)
        if l > max_cycle_length:
            max_cycle_length = l
            max_cycle_number = i

    return max_cycle_number


def is_prime(n: int) -> bool:
    """
    Check if n (n > 3) is a prime number.
    """
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False

        i += 2

    return True


def solve_on_primes() -> int:
    max_cycle_length = 0
    max_cycle_number = 0
    i = 3
    while i < 1000:
        if is_prime(i):
            l = get_cycle_length(i)
            if l > max_cycle_length:
                max_cycle_length = l
                max_cycle_number = i

        i += 2

    return max_cycle_number
