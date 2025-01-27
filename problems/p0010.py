#!/usr/bin/env python3
# coding: utf-8


"""
Summation of Primes

The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.
"""


PID = 10
ANSWER = 142913828922


MAX_NUM = 2_000_000


def solve_naive() -> int:
    basic_primes = [3, 5, 7, 11, 13, 17, 19]
    primes = basic_primes + ([0] * 220)
    prime_count = 7
    s = 2 + sum(basic_primes)
    i = primes[prime_count - 1] + 2
    while i <= MAX_NUM:
        j, is_prime = 0, True
        while j < prime_count:
            p = primes[j]
            if i % p == 0:
                is_prime = False
                break

            if p * p > i:
                break

            j += 1

        if is_prime:
            s += i
            if i * i <= MAX_NUM:
                primes[prime_count] = i
                prime_count += 1

        i += 2

    return s


def solve_sieve_with_enumerate() -> int:
    sieve = [True] * MAX_NUM
    sieve[0] = sieve[1] = False
    s = 0
    for i, is_prime in enumerate(sieve):
        if is_prime:
            s += i
            for j in range(i * i, MAX_NUM, i):
                sieve[j] = False

    return s


def solve_sieve_with_iterate() -> int:
    sieve = [True] * MAX_NUM
    sieve[0] = sieve[1] = False
    s = 0

    i = 0
    while i < MAX_NUM:
        is_prime = sieve[i]
        if is_prime:
            s += i
            for j in range(i * i, MAX_NUM, i):
                sieve[j] = False

    return s


def solve_sieve_with_slice() -> int:
    sieve = [True] * MAX_NUM
    sieve[0] = sieve[1] = False
    s = 0
    for i, is_prime in enumerate(sieve):
        if is_prime:
            s += i
            sieve[i * i:MAX_NUM:i] = [False] * len(range(i * i, MAX_NUM, i))

    return s
