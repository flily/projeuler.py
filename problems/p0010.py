#!/usr/bin/env python3
# coding: utf-8


"""
Summation of Primes

The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.
"""


PID = 10
ANSWER = 142913828922

TIMEOUT_EXT = 4000.0


def solve_naive() -> int:
    basic_primes = [3, 5, 7, 11, 13, 17, 19]
    primes = basic_primes + ([0] * 220)
    prime_count = 7
    s = 2 + sum(basic_primes)
    i = primes[prime_count - 1] + 2
    while i <= 2_000_000:
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
            if i * i <= 2_000_000:
                primes[prime_count] = i
                prime_count += 1

        i += 2

    return s
