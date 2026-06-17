#!/usr/bin/env python3
# coding: utf-8


"""
Prime Summations

It is possible to write ten as the sum of primes in exactly five different ways:
    7 + 3
    5 + 5
    5 + 3 + 2
    3 + 3 + 2 + 2
    2 + 2 + 2 + 2 + 2

What is the first value which can be written as the sum of primes in over
five thousand different ways?
"""


import functools


ANSWER = 71

LIMIT = 5000


def is_prime(n: int) -> bool:
    # assume n > 2 and n is odd
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False

        i += 2

    return True

def gen_prime_list(max_n: int) -> list[int]:
    primes = [2, 3, 5, 7, 11, 13, 17, 19]

    n = 23
    while n < max_n:
        if is_prime(n):
            primes.append(n)

        n += 2

    return primes

def count_sum_prime(primes: list[int], target: int, max_num: int) -> int:
    if target == 0:
        return 1

    count = 0
    for p in primes:
        if p > target or p > max_num:
            continue

        c = count_sum_prime(primes, target - p, p)
        count += c

    return count

def solve_naive() -> int:
    primes = gen_prime_list(100)
    primes.reverse()

    n = 11
    while True:
        got = count_sum_prime(primes, n, n - 1)
        # print(f"[{n}] => {got}")
        if got > LIMIT:
            return n

        n += 1


def count_sum_prime_cache(cache: dict[tuple[int, int], int], primes: list[int], target: int, max_num: int) -> int:
    key = (target, max_num)
    if key in cache:
        return cache[key]

    if target == 0:
        return 1

    count = 0
    for p in primes:
        if p > target or p > max_num:
            continue

        c = count_sum_prime_cache(cache, primes, target - p, p)
        count += c

    cache[key] = count
    return count

def solve_cache() -> int:
    primes = gen_prime_list(100)
    primes.reverse()

    n = 11
    cache = {}
    while True:
        got = count_sum_prime_cache(cache, primes, n, n - 1)
        # print(f"[{n}] => {got}")
        if got > LIMIT:
            return n

        n += 1


class PrimesList:
    def __init__(self, max_n: int):
        self.primes = gen_prime_list(max_n)
        self.primes.reverse()

    @functools.cache
    def count(self, target: int, max_num: int) -> int:
        if target == 0:
            return 1

        count = 0
        for p in self.primes:
            if p > target or p > max_num:
                continue

            c = self.count(target - p, p)
            count += c

        return count

def solve_cache_functools() -> int:
    primes = PrimesList(100)

    n = 11
    while True:
        got = primes.count(n, n - 1)
        # print(f"[{n}] => {got}")
        if got > LIMIT:
            return n

        n += 1
