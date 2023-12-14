#!/usr/bin/env python3
# coding: utf-8


"""
Largest Palindrome Product

A palindromic number reads the same both ways. The largest palindrome made from the product of two
2-digit numbers is 9009 = 91 × 99.

Find the largest palindrome made from the product of two 3-digit numbers.
"""


from typing import Iterator
import math


PID = 4
ANSWER = 906609


def is_palindrome_6(n: int) -> bool:
    """
    Check if n is a 6-digit palindrome
    """
    if n // 100_000 != n % 10:
        return False

    if (n // 10_000 % 10) != (n % 100 // 10):
        return False

    if (n // 1_000 % 10) != (n % 1_000 // 100):
        return False

    return True


def solve_in_integer() -> int:
    i, j = 0, 0
    while i < 999 and j < 999:
        x, y = 999 - i, 999 - j
        while x < 1000:
            n = x * y
            if is_palindrome_6(n):
                return n

            x += 1
            y -= 1

        if i == j:
            j += 1
        else:
            i += 1

    return None


def is_palindrome_string(n: int) -> bool:
    """
    Check if n is a palindrome
    """
    a = str(n)
    b = a[::-1]
    return a == b


def solve_in_string() -> int:
    i, j = 0, 0
    while i < 999 and j < 999:
        x, y = 999 - i, 999 - j
        while x < 1000:
            n = x * y
            if is_palindrome_string(n):
                return n

            x += 1
            y -= 1

        if i == j:
            j += 1
        else:
            i += 1

    return None


def solve_naive() -> int:
    for i in range(999, 99, -1):
        for j in range(999, 99, -1):
            n = i * j
            if is_palindrome_string(n):
                return n


def palindrome_gen_n(n: int) -> Iterator[int]:
    """
    Generate all palindromes below 10 ** n
    """
    if n <= 0:
        yield 1
        return

    elif n == 1:
        for x in range(2, 10):
            yield x
        return

    half_n = n // 2
    size = math.ceil(n / 2)
    x = 10 ** size - 1
    while x >= 10 ** (size - 1):
        y = 0
        for i in range(half_n):
            di = (x // (10 ** (size - i - 1))) % 10
            y += di * (10**i)

        m = x * (10**half_n) + y
        yield m
        x -= 1


def solve_by_generator() -> int:
    for n in palindrome_gen_n(6):
        # print(f"checking {n}")
        for i in range(999, 99, -1):
            # print(f"  - {i}")
            if n % i != 0:
                continue

            j = n // i
            if 100 <= j < 1000:
                return n

    return None
