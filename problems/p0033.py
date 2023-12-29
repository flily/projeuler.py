#!/usr/bin/env python3
# coding: utf-8


"""
Digit Cancelling Fractions

The fraction 49/98 is a curious fraction, as an inexperienced mathematician in attempting to
simplify it may incorrectly believe that 49/98 = 4/8, which is correct, is obtained by cancelling
the 9s.

We shall consider fractions like, 30/50 = 3/5, to be trivial examples.

There are exactly four non-trivial examples of this type of fraction, less than one in value, and
containing two digits in the numerator and denominator.

If the product of these four fractions is given in its lowest common terms, find the value of the
denominator.
"""


ANSWER = 100


def cancel_fractions(m: int, n: int) -> tuple[int, int]:
    """
    Cancel fractions
    """
    m1, m2 = m // 10, m % 10
    n1, n2 = n // 10, n % 10

    if m1 == n1:
        return m2, n2

    if m1 == n2:
        return m2, n1

    if m2 == n1:
        return m1, n2

    if m2 == n2:
        return m1, n1

    return None


def solve() -> int:
    p, q = 1, 1
    for m in range(10, 100):
        for n in range(m + 1, 100):
            if m % 10 == 0 and n % 10 == 0:
                continue

            result = cancel_fractions(m, n)
            if result is None:
                continue

            m1, n1 = result
            if m * n1 == n * m1:
                p *= m1
                q *= n1

    return q // p
