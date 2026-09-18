#!/usr/bin/env python3
# coding: utf-8


"""
Largest Prime Factor

The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143?
"""


from typing import List
import bisect


PID = 3
ANSWER = 6857


NUMBER = 600851475143


def is_prime(n: int) -> bool:
    """
    Check if n (positive) is a prime
    """
    if n <= 2:
        return True

    i = 3
    while i * i <= n:
        if n % i == 0:
            return False

        i += 2

    return True


# checked in rust version, cost ~105s.
def solve_naive() -> int:
    n = NUMBER
    i = 3
    last = 3
    while 2 * i <= n:
        if n % i == 0 and is_prime(i):
            last = i

        i += 2

    return last


def remove_factor(n: int, f: int) -> int:
    """
    Remove all factors of n
    """
    while n % f == 0:
        n //= f

    return n


def solve_by_remove_factor() -> int:
    n = NUMBER
    i = 3
    last = 3
    while n > 0 and i <= n:
        if n % i == 0 and is_prime(i):
            last = i
            n = remove_factor(n, i)

        i += 2

    return last


class PrimeTable:
    """
    Prime table
    """

    def __init__(self, primes: List[int]):
        self.primes = primes
        self.primes.sort()
        self.prime_set = set(primes)
        self.largest = self.primes[-1]

    def check_prime(self, n: int) -> bool:
        """
        Check if n is a prime
        """
        if n <= self.largest:
            return n in self.prime_set

        for p in self.primes:
            if n % p == 0:
                return False

        self.primes.append(n)
        self.prime_set.add(n)
        return True


class PrimeList:
    """
    Prime list
    """
    def __init__(self, primes: List[int]):
        self.size = 1000
        self.primes = [0] * 1000
        self.count = len(primes)
        for i in range(self.count):
            self.primes[i] = primes[i]

    def add(self, p: int):
        if self.count >= len(self.primes):
            self.primes.extend([0] * self.size)

        self.primes[self.count] = p
        self.count += 1

    def check_prime(self, n: int) -> bool:
        """
        Check if n is a prime
        """
        largest = self.primes[self.count - 1]
        if n <= largest:
            index = bisect.bisect(self.primes, n, 0, self.count)
            return self.primes[index] == n

        for i in range(self.count):
            p = self.primes[i]
            if n % p == 0:
                return False

        self.add(n)
        return True


def find_largest_prime_factor(primes: PrimeTable | PrimeList, n: int) -> int:
    """
    Find largest prime factor of n
    """
    factors = []
    if n % 2 == 0:
        factors.append(2)
        n = remove_factor(n, 2)

    i = 3
    while n > 0 and i <= n:
        # check prime first to make prime list correct
        if primes.check_prime(i) and n % i == 0:
            factors.append(i)
            n = remove_factor(n, i)

        i += 2

    if len(factors) <= 0:
        return 0

    return factors[-1]


def solve_by_prime_table() -> int:
    primes_base = [3, 5, 7, 11, 13, 17, 19]
    primes = PrimeTable(primes_base)

    return find_largest_prime_factor(primes, NUMBER)


def solve_by_prime_list() -> int:
    primes_base = [3, 5, 7, 11, 13, 17, 19]
    primes = PrimeList(primes_base)

    return find_largest_prime_factor(primes, NUMBER)


def find_largest_prime_factor_by_sieve(n: int) -> int:
    sqrt = int(n**0.5)
    sieve = [True] * (sqrt + 1)
    sieve[0] = False

    m = n
    p, mp = 3, 3
    while p * p < m:
        if sieve[p // 2]:
            if m % p == 0:
                m = remove_factor(m, p)
                sqrt = int(m**0.5)
                mp = p

            for i in range(p * p, sqrt, p):
                sieve[i // 2] = False

        p += 2

    return mp


def solve_by_sieve() -> int:
    return find_largest_prime_factor_by_sieve(NUMBER)
