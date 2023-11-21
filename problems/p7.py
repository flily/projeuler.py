#!/usr/bin/env python3
# coding: utf-8


"""
10001st Prime

By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.

What is the 10001st prime number?
"""


PID = 7
ANSWER = 104743

PRIME_COUNT = 10001


def solve_with_filter() -> int:
    primes = [11, 13, 17, 19]
    i = primes[-1] + 2
    p3, p5, p7 = 2, 2, 6
    while len(primes) < PRIME_COUNT - 4:
        p3 = (p3 + 1) % 3
        p5 = (p5 + 1) % 5
        p7 = (p7 + 1) % 7

        if p3 == 0 or p5 == 0 or p7 == 0:
            i += 2
            continue

        is_prime = True
        for p in primes:
            if i % p == 0:
                is_prime = False
                break

            if p * p > i:
                break

        if is_prime:
            primes.append(i)

        i += 2

    return primes[-1]


def solve_with_filter_and_prealloc_space() -> int:
    primes = [11, 13, 17, 19] + ([0] * (PRIME_COUNT - 8))
    c = 4
    i = 21
    p3, p5, p7 = 2, 2, 6
    while c < PRIME_COUNT - 4:
        p3 = (p3 + 1) % 3
        p5 = (p5 + 1) % 5
        p7 = (p7 + 1) % 7

        if p3 == 0 or p5 == 0 or p7 == 0:
            i += 2
            continue

        is_prime = True
        j = 0
        while j < c:
            p = primes[j]
            if i % p == 0:
                is_prime = False
                break

            if p * p > i:
                break

            j += 1

        if is_prime:
            primes[c] = i
            c += 1

        i += 2

    return primes[-1]


def solve_naive() -> int:
    primes = [3, 5, 7, 11, 13, 17, 19]
    i = primes[-1]
    while len(primes) < PRIME_COUNT:
        is_prime = True
        for p in primes:
            if i % p == 0:
                is_prime = False
                break

            if p * p > i:
                break

        if is_prime:
            primes.append(i)

        i += 2

    return primes[-1]


def solve_naive_with_prealloc_space() -> int:
    primes = [3, 5, 7, 11, 13, 17, 19] + ([0] * (PRIME_COUNT - 8))
    c = 7
    i = primes[6] + 2
    while c < PRIME_COUNT - 1:
        is_prime = True
        for p in primes:
            if i % p == 0:
                is_prime = False
                break

            if p * p > i:
                break

        if is_prime:
            primes[c] = i
            c += 1

        i += 2

    return primes[-1]

