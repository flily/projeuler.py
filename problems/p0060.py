#!/usr/bin/env python3
# coding: utf-8


"""
Prime Pair Sets

The primes 3, 7, 109, and 673, are quite remarkable. By taking any two primes and concatenating
them in any order the result will always be prime. For example, taking 7 and 109, both 7109 and
1097 are prime. The sum of these four primes, 792, represents the lowest sum for a set of four
primes with this property.

Find the lowest sum for a set of five primes for which any two primes concatenate to produce
another prime.
"""


from typing import Iterable, Iterator
import itertools


ANSWER = None


def make_primes(max_num: int) -> Iterable[int]:
    """
    Make a prime cache
    """
    primes = [2, 3, 5, 7, 11, 13, 17, 19]
    n = 21
    while n < max_num:
        i = 1
        checked = True
        while i < len(primes):
            p = primes[i]
            if p * p > n:
                break

            if n % p == 0:
                checked = False
                break

            i += 1

        if checked:
            primes.append(n)

        n += 2

    return primes


def find_sub_numbers(n: int) -> Iterator[tuple[int, int, int]]:
    """
    Find all sub numbers of n.
    """
    s = str(n)
    l = len(s)
    for i in range(1, l):
        if s[i] == "0":
            continue

        a = int(s[:i])
        b = int(s[i:])
        c = int(s[i:] + s[:i])
        yield a, b, c


def solve() -> int:
    primes = make_primes(100000)
    prime_set = set(primes)
    print(f"primes: {len(primes)}, last={primes[-1]}")
    prime_group = {}
    prime_group_map= {}
    c = 0
    for p in primes:
        for sub_a, sub_b, rev in find_sub_numbers(p):
            if rev not in prime_set:
                continue

            if sub_a not in prime_set or sub_b not in prime_set:
                continue

            if sub_a > sub_b:
                continue

            print(f"{p}: {sub_a}, {sub_b}, {rev}")
            c += 1

    return c
