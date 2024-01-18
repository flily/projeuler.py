#!/usr/bin/env python3
# coding: utf-8


"""
Consecutive Prime Sum

The prime 41, can be written as the sum of six consecutive primes:
            41 = 2 + 3 + 5 + 7 + 11 + 13

This is the longest sum of consecutive primes that adds to a prime below one-hundred.

The longest sum of consecutive primes below one-thousand that adds to a prime, contains 21 terms,
and is equal to 953.

Which prime, below one-million, can be written as the sum of the most consecutive primes?
"""


from typing import Iterable


ANSWER = 997651

LIMIT = 1_000_000


def is_prime(primes: Iterable[int], n: int) -> bool:
    """
    Check if n (n >= 3) is prime.
    """
    i = 0
    while i < len(primes):
        p = primes[i]
        if p * p > n:
            break

        if n % p == 0:
            return False

        i += 1

    return True


def build_primes_below(n: int) -> Iterable[int]:
    """
    Build a list of primes below n.
    """
    primes = [2, 3, 5, 7, 11, 13, 17, 19]
    i = 21
    while i < n:
        if is_prime(primes, i):
            primes.append(i)

        i += 2

    return primes


def find_prime_sum_seq(primes: Iterable[int], n: int, min_start: int = 2) -> int:
    """
    Find the prime sum sequence of n.
    """
    for length in range(min_start, len(primes)):
        for i in range(len(primes) - length):
            if n == sum(primes[i : i + length]):
                return length

    return 0


def solve_naive() -> int:
    primes = build_primes_below(1_000_000)
    max_length = 953
    max_length_prime = 21
    for prime in primes:
        length = find_prime_sum_seq(primes, prime)
        if length > max_length:
            max_length_prime = prime
            max_length = length

    return max_length_prime


def build_primes_below_prealloc(n: int) -> Iterable[int]:
    """
    Build a list of primes below n.
    """
    primes = [2, 3, 5, 7, 11, 13, 17, 19] + ([0] * 5_000)
    length = 8
    i = 21
    while i < n:
        if is_prime(primes, i):
            primes[length] = i
            length += 1

        i += 2

    return primes[:length]


def solve_compare_sum() -> int:
    primes = build_primes_below_prealloc(1_000_000 // 21)
    max_length = 21
    max_length_prime = 953
    for end in range(len(primes), 21, -1):
        s = 0
        start = end
        while start > 0:
            p = primes[start - 1]
            if s + p > 1_000_000:
                break

            s += p
            start -= 1

        if end - start < max_length:
            continue

        if end < max_length:
            break

        while start < end:
            if is_prime(primes, s):
                length = end - start
                if length > max_length:
                    max_length_prime = s
                    max_length = length

                break
            s -= primes[start]
            start += 1

    return max_length_prime
