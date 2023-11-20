#!/usr/bin/env python3
# coding: utf-8


"""
Largest Palindrome Product

A palindromic number reads the same both ways. The largest palindrome made from the product of two
2-digit numbers is 9009 = 91 × 99.

Find the largest palindrome made from the product of two 3-digit numbers.
"""


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
