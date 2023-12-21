#!/usr/bin/env python3
# coding: utf-8


"""
1000-digit Fibonacci number

The Fibonacci sequence is defined by the recurrence relation:
    F(n) = F(n-1) + F(n-2), where F(1) = 1 and F(2) = 1.

Hence the first 12 terms will be:
        F(1) = 1
        F(2) = 1
        F(3) = 2
        F(4) = 3
        F(5) = 5
        F(6) = 8
        F(7) = 13
        F(8) = 21
        F(9) = 34
        F(10) = 55
        F(11) = 89
        F(12) = 144
The 12th term, F(12), is the first term to contain three digits.
What is the index of the first term in the Fibonacci sequence to contain 1000 digits?
"""


import math


PID = 25
ANSWER = 4782


def solve_naive() -> int:
    fibos = [1, 1]
    while math.log10(fibos[-1]) < 999:
        # 10 ** 999 is larger than the maximun double-precision floating-point number.
        # But math.log10() handles it correctly, standard library can process bit integer well.
        fibos.append(fibos[-1] + fibos[-2])

    return len(fibos)


def solve_without_array() -> int:
    a, b = 1, 1
    i = 2
    while math.log10(b) < 999:
        a, b = b, a + b
        i += 1

    return i
