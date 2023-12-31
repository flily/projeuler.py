#!/usr/bin/env python3
# coding: utf-8


"""
Double-base Palindromes

The decimal number, 585 = 1001001001 (binary), is palindromic in both bases.

Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2.

(Please note that the palindromic number, in either base, may not include leading zeros.)
"""


import math
from typing import Iterator


ANSWER = 872187


def is_palindrome_10(n: int) -> bool:
    """
    Check if n is a decimal palindrome
    """
    size = math.floor(math.log10(n)) + 1
    for i in range(size // 2):
        dl = n // (10**i) % 10
        dr = n // (10 ** (size - i - 1)) % 10
        if dl != dr:
            return False

    return True


def is_palindrome_2(n: int) -> bool:
    """
    Check if n is a binary palindrome
    """
    size = math.floor(math.log2(n)) + 1
    for i in range(size // 2):
        dl = (n & (2**i)) == 0
        dr = (n & (2 ** (size - i - 1))) == 0
        if dl != dr:
            return False

    return True


def solve_naive() -> int:
    result = 0
    for n in range(1, 1_000_000):
        if is_palindrome_10(n) and is_palindrome_2(n):
            result += n

    return result


def palindrome_gen_n(n: int) -> Iterator[int]:
    """
    Generate all palindromes below 10 ** n
    """
    if n <= 0:
        yield 1
        return

    if n == 1:
        for x in range(2, 10):
            yield x
        return

    half_n = n // 2
    size = math.ceil(n / 2)
    for x in range(10 ** (size - 1), 10**size):
        y = 0
        for i in range(half_n):
            di = (x // (10 ** (size - i - 1))) % 10
            y += di * (10**i)

        m = x * (10**half_n) + y
        yield m


def solve_by_generator() -> int:
    result = 0
    for i in range(7):
        for n in palindrome_gen_n(i):
            if is_palindrome_10(n) and is_palindrome_2(n):
                result += n

    return result
