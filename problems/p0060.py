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


from typing import Generator

import itertools


ANSWER = 26033

TOTAL_NUMS = 5


def gen_primes(n: int) -> tuple[list[int], set[int]]:
    """
    Generate prime numbers up to max_num.
    """
    sieve = [True] * (n // 2)
    for i in range(3, int(n ** 0.5) + 1, 2):
        if sieve[i // 2]:
            sieve[i * i // 2::i] = [False] * ((n - i * i - 1) // (2 * i) + 1)

    primes = [2 * i + 1 for i in range(1, n // 2) if sieve[i]]
    return primes, set(primes)


def is_prime(prime_list: list[int], prime_set: set[int], n: int) -> bool:
    """
    Check if n is a prime number.
    """
    if n in prime_set:
        return True

    i, p = 0, 3
    l = len(prime_list)
    while i < l:
        p = prime_list[i]
        if p * p > n:
            return True

        if n % p == 0:
            return False

        i += 1

    return True


def solve_naive() -> int:
    primes, prime_set = gen_primes(100_000_000)
    main_primes = [x for x in primes if x < 10_000]

    prime_pairs = set()
    prime_pair_map = {}
    for a, b in itertools.combinations(main_primes, 2):
        ab = int(f"{a}{b}")
        ba = int(f"{b}{a}")

        if is_prime(primes, prime_set, ab) and is_prime(primes, prime_set, ba):
            # print(f"found: {a} {b} {ab} {ba}")
            prime_pairs.add((a, b))
            prime_pair_map.setdefault(a, set()).add(b)
            prime_pair_map.setdefault(b, set()).add(a)

    possible_primes = set()
    for k, v in prime_pair_map.items():
        if len(v) >= TOTAL_NUMS - 1:
            possible_primes.add(k)

    possible_prime_map = {}
    for k, v in prime_pair_map.items():
        if k not in possible_primes:
            continue

        possible_prime_map[k] = [x for x in (v & possible_primes | set([k])) if x >= k]
        possible_prime_map[k].sort()

    min_sum = -1
    possible_prime_list = list(possible_prime_map.keys())
    possible_prime_list.sort()
    for k in possible_prime_list:
        v = possible_prime_map[k]
        for group in itertools.combinations(v, TOTAL_NUMS):
            first = group[0]

            if sum(group) > min_sum > 0:
                break

            if min_sum > 0 and first > min_sum / len(group):
                break

            found = True
            for a, b in itertools.combinations(group, 2):
                if (a, b) not in prime_pairs:
                    found = False
                    break

            if found:
                s = sum(group)
                if min_sum < 0:
                    min_sum = sum(group)
                else:
                    min_sum = min(min_sum, s)

    return min_sum


def find_prime_pair_set(
        prime_pairs: set[int], 
        primes: list[int],
        current: list[int],
        length: int,
        index: int,
    ) -> Generator[list[int]]:
    """
    Find prime pair set.
    """
    if len(current) == length:
        yield current
        return

    i = index
    while i < len(primes):
        p = primes[i]
        found = True
        for n in current:
            if (n, p) not in prime_pairs:
                found = False
                break

        if found:
            for x in find_prime_pair_set(prime_pairs, primes, current + [p], length, i + 1):
                yield x

        i += 1


def solve_optimized() -> int:
    primes, prime_set = gen_primes(100_000_000)

    main_primes = [x for x in primes if x < 10_000]
    prime_pairs = set()
    prime_pair_map = {}
    for a, b in itertools.combinations(main_primes, 2):
        ab = int(f"{a}{b}")
        ba = int(f"{b}{a}")

        if is_prime(primes, prime_set, ab) and is_prime(primes, prime_set, ba):
            prime_pairs.add((a, b))
            prime_pair_map.setdefault(a, set()).add(b)
            prime_pair_map.setdefault(b, set()).add(a)

    possible_primes = set()
    for k, v in prime_pair_map.items():
        if len(v) >= TOTAL_NUMS - 1:
            possible_primes.add(k)

    possible_prime_map = {}
    for k, v in prime_pair_map.items():
        if k not in possible_primes:
            continue

        possible_prime_map[k] = [x for x in (v & possible_primes | set([k])) if x >= k]
        possible_prime_map[k].sort()

    possible_prime_list = list(possible_prime_map.keys())
    possible_prime_list.sort()
    for x in find_prime_pair_set(prime_pairs, possible_prime_list, [], TOTAL_NUMS, 0):
        return sum(x)

    return -1
