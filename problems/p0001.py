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


def solve_naive() -> int:
    i = 3
    s = 0
    while i < 1000:
        if i % 3 == 0 or i % 5 == 0:
            s += i

        i += 1

    return s


def sum_of_multiples(n: int, k: int) -> int:
    m = (n - 1) // k
    return k * m * (m + 1) // 2

def solve_formula() -> int:
    return sum_of_multiples(1000, 3) + sum_of_multiples(1000, 5) - sum_of_multiples(1000, 15)
