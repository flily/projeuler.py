#!/usr/bin/env python3
# coding: utf-8


"""
Lychrel Numbers

If we take 47, reverse and add, 47 + 74 = 121, which is palindromic.

Not all numbers produce palindromes so quickly. For example,
             349 + 943 = 1292
            1292 + 2921 = 4213
            4213 + 3124 = 7337

That is, 349 took three iterations to arrive at a palindrome.

Although no one has proved it yet, it is thought that some numbers, like 196, never produce a
palindrome. A number that never forms a palindrome through the reverse and add process is called a
Lychrel number. Due to the theoretical nature of these numbers, and for the purpose of this
problem, we shall assume that a number is Lychrel until proven otherwise. In addition you are given
that for every number below ten-thousand, it will either (i) become a palindrome in less than fifty
iterations, or, (ii) no one, with all the computing power that exists, has managed so far to map it
to a palindrome. In fact, 10677 is the first number to be shown to require over fifty iterations
before producing a palindrome: 4668731596684224866951378664 (53 iterations, 28-digits).

Surprisingly, there are palindromic numbers that are themselves Lychrel numbers; the first example
is 4994.

How many Lychrel numbers are there below ten-thousand?

NOTE: Wording was modified slightly on 24 April 2007 to emphasise the theoretical nature of
Lychrel numbers.
"""


import math


ANSWER = 249


def make_palindrome(n: int) -> int:
    """
    Make a palindrome from n.
    """
    size = math.floor(math.log10(n)) + 1
    result = 0

    for i in range(size):
        digit = n // (10**i) % 10
        result += digit * 10 ** (size - i - 1)

    return result


def is_palindrome(n: int) -> bool:
    """
    Check if n is a palindrome.
    """
    size = math.floor(math.log10(n)) + 1
    for i in range(size // 2):
        dh = n // 10 ** (size - i - 1) % 10
        dl = n // 10**i % 10
        if dh != dl:
            return False

    return True


def is_lychrel(n: int) -> bool:
    """
    Check if n is a Lychrel number.
    """
    for _ in range(50):
        m = make_palindrome(n)
        p = n + m
        if is_palindrome(p):
            return False


        n = p

    return True


def solve() -> int:
    result = 0
    for i in range(1, 10000):
        if is_lychrel(i):
            result += 1

    return result
