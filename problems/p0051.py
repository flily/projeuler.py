#!/usr/bin/env python3
# coding: utf-8


"""
Prime Digit Replacements

By replacing the 1st digit of the 2-digit number *3, it turns out that six of the nine possible
values: 13, 23, 43, 53, 73, and 83, are all prime.

By replacing the 3rd and 4th digits of 56**3 with the same digit, this 5-digit number is the first
example having seven primes among the ten generated numbers, yielding the family: 56003, 56113,
56333, 56443, 56663, 56773, and 56993. Consequently 56003, being the first member of this family,
is the smallest prime with this property.

Find the smallest prime which, by replacing part of the number (not necessarily adjacent digits)
with the same digit, is part of an eight prime value family.
"""


from typing import Iterable, Iterator


ANSWER = 121313


def is_prime(n: int) -> bool:
    """
    Check if n (n >= 3) is prime.
    """
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False

        i += 2

    return True


def get_number_families(n: int) -> Iterable[str]:
    """
    Get the number families of n.
    """
    set_digit = set()
    result = set()
    s = str(n)
    for digit in s:
        if digit in set_digit:
            continue

        set_digit.add(digit)
        result.add(s.replace(digit, '*'))

    return result


def get_family_numbers(n: str) -> Iterator[int]:
    """
    Get the family numbers of n.
    """
    for i in range(10):
        if i == 0 and n[0] == '*':
            continue

        yield int(n.replace('*', str(i)))


def solve_naive() -> int:
    n = 11
    while True:
        if is_prime(n):
            families = get_number_families(n)
            for family in families:
                c = 0
                for number in get_family_numbers(family):
                    if is_prime(number):
                        c += 1

                if c == 8:
                    return n

        n += 2
