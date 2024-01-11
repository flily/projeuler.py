#!/usr/bin/env python3
# coding: utf-8


"""
Goldbach's Other Conjecture

It was proposed by Christian Goldbach that every odd composite number can be written as the sum of
a prime and twice a square.
             9 =  7 + 2 × 1^2
            15 =  7 + 2 × 2^2
            21 =  3 + 2 × 3^2
            25 =  7 + 2 × 3^2
            27 = 19 + 2 × 2^2
            33 = 31 + 2 × 1^2

It turns out that the conjecture was false.

What is the smallest odd composite that cannot be written as the sum of a prime and twice a square?
"""


ANSWER = 5777


def is_prime(n: int) -> bool:
    """
    Check if n (MUST BE an odd) is prime.
    """
    if n < 2:
        return False

    if n == 2:
        return True

    i = 3
    while i * i <= n:
        if n % i == 0:
            return False

        i += 2

    return True


def is_integer_double_square(n: int) -> bool:
    """
    Check if n is an integer square.
    """
    if n % 2 != 0:
        return False

    h = n // 2
    s = h**0.5
    return s == int(s)


def is_goldbach(n: int) -> bool:
    """
    Check if n (an odd) is a Goldbach number.
    """
    if is_integer_double_square(n - 2):
        return True

    i = 3
    while i <= n - 2:
        if is_prime(i) and is_integer_double_square(n - i):
            return True

        i += 2

    return False


def solve_naive() -> int:
    result = 9
    while True:
        if not is_prime(result) and not is_goldbach(result):
            break

        result += 2

    return result
