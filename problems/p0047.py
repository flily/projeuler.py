#!/usr/bin/env python3
# coding: utf-8


"""
Distinct Primes Factors

The first two consecutive numbers to have two distinct prime factors are:
            14 = 2 × 7
            15 = 3 × 5

The first three consecutive numbers to have three distinct prime factors are:
            644 = 2^2 × 7 × 23
            645 = 3 × 5 × 43
            646 = 2 × 17 × 19

Find the first four consecutive integers to have four distinct prime factors each. What is the
first of these numbers?
"""


ANSWER = 134043


def is_prime(n: int) -> bool:
    """
    Check if n (n >= 3) is prime.
    """
    if n % 2 == 0:
        return False

    i = 3
    while i * i <= n:
        if n % i == 0:
            return False

        i += 2

    return True


def find_prime_factors(n: int) -> set[int]:
    """
    Find the prime factors of n.
    """
    result = set()
    if n % 2 == 0:
        result.add(2)
        if is_prime(n // 2):
            result.add(n // 2)

    i = 3
    while i * i <= n:
        if n % i == 0:
            if is_prime(i):
                result.add(i)
            if i * i != n and is_prime(n // i):
                result.add(n // i)

        i += 1

    return result

def solve_naive() -> int:
    n = 647
    c = 0

    while True:
        pfs = find_prime_factors(n)
        if len(pfs) == 4:
            c += 1
        else:
            c = 0

        if c == 4:
            break

        n += 1

    return n - 3


def remove_factor(n: int, f: int) -> int:
    while n % f == 0:
        n //= f

    return n


def find_prime_factors_remove_factor(n: int) -> set[int]:
    result = set()
    m = n
    if m % 2 == 0:
        result.add(2)
        m = remove_factor(m, 2)

    i = 3
    while i * i <= n:
        if n % i == 0:
            if is_prime(i):
                result.add(i)
                m = remove_factor(m, i)

        i += 2

    if m > 1:
        result.add(m)

    return result


def solve_remove_factor() -> int:
    n = 647
    c = 0

    while True:
        pfs = find_prime_factors_remove_factor(n)
        if len(pfs) == 4:
            c += 1
        else:
            c = 0

        if c == 4:
            break

        n += 1

    return n - 3


def find_prime_factors_count_only(n: int) -> set[int]:
    result = 0
    m = n
    if m % 2 == 0:
        result += 1
        m = remove_factor(m, 2)

    i = 3
    while i * i <= n:
        if n % i == 0:
            if is_prime(i):
                result += 1
                m = remove_factor(m, i)

        i += 2

    if m > 1:
        result += 1

    return result


def solve_count_only() -> int:
    n = 647
    c = 0

    while True:
        pfs_count = find_prime_factors_count_only(n)
        if pfs_count == 4:
            c += 1
        else:
            c = 0

        if c == 4:
            break

        n += 1

    return n - 3


def build_primes_list(max_prime: int) -> list[int]:
    result = [2, 3, 5, 7, 11, 13, 17, 19]

    i = 23
    while i <= max_prime:
        check_prime = True
        for p in result:
            if p * p > i:
                break

            if i % p == 0:
                check_prime = False
                break

        if check_prime:
            result.append(i)

        i += 2

    return result


def find_prime_factors_count_with_prime_list(primes: list[int], n: int) -> int:
    result = 0
    m = n

    for p in primes:
        if p * p > m:
            break

        if n % p == 0:
            result += 1
            m = remove_factor(m, p)

    if m > 1:
        result += 1

    return result


def solve_prime_list() -> int:
    n = 647
    c = 0

    primes = build_primes_list(1000)

    while True:
        pfs_count = find_prime_factors_count_with_prime_list(primes, n)

        if pfs_count == 4:
            c += 1
        else:
            c = 0

        if c == 4:
            break

        n += 1

    return n - 3
