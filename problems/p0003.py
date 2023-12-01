#!/usr/bin/env python3
# coding: utf-8


"""
Largest Prime Factor

The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143?
"""


from typing import List


PID = 3
ANSWER = 6857


def remove_factor(n: int, f: int) -> int:
    """
    Remove all factors of n
    """
    while n % f == 0:
        n //= f

    return n


class PrimeTable:
    """
    Prime table
    """

    def __init__(self, primes: List[int]):
        self.prime_list = primes
        self.prime_list.sort()
        self.prime_set = set(primes)
        self.largest = self.prime_list[-1]

    def check_prime(self, n: int) -> bool:
        """
        Check if n is a prime
        """
        if n <= self.largest:
            return n in self.prime_set

        for p in self.prime_list:
            if n % p == 0:
                return False

        self.prime_list.append(n)
        self.prime_set.add(n)
        return True


def find_largest_prime_factor(primes: PrimeTable, n: int) -> int:
    """
    Find largest prime factor of n
    """
    factors = []
    if n % 2 == 0:
        factors.append(2)
        n = remove_factor(n, 2)

    i = 3
    while i * i <= n:
        if primes.check_prime(i):
            if n % i == 0:
                factors.append(i)
                n = remove_factor(n, i)

        i += 2

    if i < n:
        factors.append(n)

    if len(factors) <= 0:
        return 0

    return factors[-1]


def solve() -> int:
    primes_base = [3, 5, 7, 11, 13, 17, 19]
    primes = PrimeTable(primes_base)

    return find_largest_prime_factor(primes, 600851475143)
