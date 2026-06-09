#!/usr/bin/env python3
# coding: utf-8


"""
Digit Factorial Chains

The number 145 is well known for the property that the sum of the factorial of its digits is equal
to 145:
    1! + 4! + 5! = 1 + 24 + 120 = 145

Perhaps less well known is 169, in that it produces the longest chain of numbers that link back to
169; it turns out that there are only three such loops that exist:
    169 -> 363601 -> 1454 -> 169
    871 -> 45361 -> 871
    872 -> 45362 -> 872

It is not difficult to prove that EVERY starting number will eventually get stuck in a loop.
For example,
    63 -> 363600 -> 1454 -> 169 -> 363601 (-> 1454)
    78 -> 45360 -> 871 -> 45361 (-> 871)
    540 -> 145 (-> 145)

Starting with 69 produces a chain of five non-repeating terms, but the longest non-repeating chain
with a starting number below one million is sixty terms.

How many chains, with a starting number below one million, contain exactly sixty non-repeating
terms?
"""


ANSWER = 402


def factorial(n: int) -> int:
    if n == 0:
        return 1

    result = 1
    for i in range(2, n + 1):
        result *= i

    return result


def factorial_sum(n: int) -> int:
    s = 0
    while n > 0:
        d = n % 10
        s += factorial(d)
        n //= 10

    return s


def check_chain_naive(n: int) -> int:
    seen = set()
    m = n
    while m not in seen:
        seen.add(m)
        m = factorial_sum(m)

    return len(seen)


def solve_naive() -> int:
    count = 0
    for n in range(1, 1_000_000):
        if check_chain_naive(n) == 60:
            count += 1

    return count


FACTORIAL_TABLE = {
    0: 1,
    1: 1,
    2: 2,
    3: 6,
    4: 24,
    5: 120,
    6: 720,
    7: 5040,
    8: 40320,
    9: 362880
}


def factorial_sum_table(n: int) -> int:
    s = 0
    while n > 0:
        d = n % 10
        s += FACTORIAL_TABLE[d]
        n //= 10

    return s


def check_chain_table(n: int) -> int:
    seen = set()
    m = n
    while m not in seen:
        seen.add(m)
        m = factorial_sum_table(m)

    return len(seen)


def solve_factorial_table() -> int:
    count = 0
    for n in range(1, 1_000_000):
        if check_chain_table(n) == 60:
            count += 1

    return count


def check_chain_cache(n: int, cache: dict[int, int]) -> int:
    seen = set()
    m = n
    while m not in seen:
        if m in cache:
            r =len(seen) + cache[m]
            cache[n] = r
            return r

        seen.add(m)
        m = factorial_sum_table(m)

    result = len(seen)
    cache[n] = result
    return result


def solve_table() -> int:
    cache = {}
    count = 0

    for n in range(1, 1_000_000):
        if check_chain_cache(n, cache) == 60:
            count += 1

    return count
