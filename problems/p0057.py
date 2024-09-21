#!/usr/bin/env python3
# coding: utf-8


"""
Square root convergents

It is possible to show that the square root of two can be expressed as an infinite continued
fraction.
            √2 = 1 + 1 / (2 + 1 / (2 + 1 / (2 + ...)))

By expanding this for the first four iterations, we get:
    1 + 1 / 2 = 3 / 2 = 1.5
    1 + 1 / (2 + 1 / 2) = 7 / 5 = 1.4
    1 + 1 / (2 + 1 / (2 + 1 / 2)) = 17 / 12 = 1.41666...
    1 + 1 / (2 + 1 / (2 + 1 / (2 + 1 / 2))) = 41 / 29 = 1.41379...

The next three expansions are 99 / 70, 239 / 169, and 577 / 408, but the eighth expansion,
1393 / 985, is the first example where the number of digits in the numerator exceeds the number of
digits in the denominator.

In the first one-thousand expansions, how many fractions contain a numerator with more digits than
denominator?
"""


from __future__ import annotations

from typing import Iterator

import math


ANSWER = 153


class Fraction:
    """
    A fraction number.
    """

    def __init__(self, numerator: int, denominator: int = 1):
        self.numerator = numerator
        self.denominator = denominator

    def __repr__(self) -> str:
        return f"{self.numerator} / {self.denominator}"

    def __add__(self, other: Fraction) -> Fraction:
        n = self.numerator * other.denominator + self.denominator * other.numerator
        d = self.denominator * other.denominator
        return Fraction(n, d)

    def __truediv__(self, other: Fraction) -> Fraction:
        n = self.numerator * other.denominator
        d = self.denominator * other.numerator
        return Fraction(n, d)


def expand(n: int) -> Fraction:
    """
    Expand the square root of n.
    """
    if n == 1:
        return Fraction(1) + Fraction(1, 2)

    s = Fraction(1) / (Fraction(2) + Fraction(1, 2))
    while n > 1:
        s = Fraction(1) / (Fraction(2) + s)
        n -= 1

    return Fraction(1) + s


def solve_naive() -> int:
    result = 0
    for i in range(1, 1001):
        n = expand(i)
        size_numerator = math.floor(math.log10(n.numerator)) + 1
        size_denominator = math.floor(math.log10(n.denominator)) + 1
        if size_numerator > size_denominator:
            result += 1

    return result


def expand_generator() -> Iterator[Fraction]:
    """
    Expand the square root of 2.
    """
    yield Fraction(3, 2)

    n = Fraction(1, 2)
    while True:
        n = Fraction(1) / (Fraction(2) + n)
        yield Fraction(1) + n


def solve_with_generator() -> int:
    result = 0
    count = 0
    for n in expand_generator():
        count += 1
        size_numerator = math.floor(math.log10(n.numerator)) + 1
        size_denominator = math.floor(math.log10(n.denominator)) + 1
        if size_numerator > size_denominator:
            result += 1

        if count >= 1000:
            break

    return result


def direct_generator() -> Iterator[int]:
    """
    Directly calculate the expansion.
    """
    yield 3, 2

    n, d = 2, 5
    while True:
        yield d + n, d
        n, d = d, d * 2 + n


def solve_directly_calculate() -> int:
    result = 0
    count = 0
    for n, d in direct_generator():
        count += 1
        size_numerator = math.floor(math.log10(n)) + 1
        size_denominator = math.floor(math.log10(d)) + 1
        if size_numerator > size_denominator:
            result += 1

        if count >= 1000:
            break

    return result


if __name__ == "__main__":
    ANSWER = solve_with_generator()
    print(f"Answer: {ANSWER}")
