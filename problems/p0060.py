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
TIMEOUT_EXT = {
    "optimized": 6000.0
}

TOTAL_NUMS = 5


def gen_primes_sieve(n: int) -> list[int]:
    """
    Generate prime numbers up to max_num.
    """
    sieve = [True] * (n // 2)
    for i in range(3, int(n ** 0.5) + 1, 2):
        if sieve[i // 2]:
            sieve[i * i // 2::i] = [False] * ((n - i * i - 1) // (2 * i) + 1)

    return sieve

def is_prime_in_sieve(sieve: list[bool], n: int) -> bool:
    """
    Check if n is a prime number using sieve.
    """
    if n == 2:
        return True

    if n < 2 or n % 2 == 0:
        return False

    return sieve[n // 2]


def is_prime_in_list(prime_list: list[int], n: int) -> bool:
    """
    Check if n is a prime number.
    """
    for p in prime_list:
        if p * p > n:
            return True

        if n % p == 0:
            return False

    return True


def is_prime(n: int) -> bool:
    """
    Check if n is a prime number.
    """
    if n <= 1:
        return False

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    i = 3
    while i * i <= n:
        if n % i == 0:
            return False

        i += 2

    return True


# checked, correct
# Python 3.14: ~150s
# PyPy 7.3 (3.10): ~62s
def solve_naive() -> int:
    """
    naive: check all prime combinations
    """
    prime_sieve = gen_primes_sieve(10_000)
    primes = [2 * i + 1 for i in range(1, len(prime_sieve)) if prime_sieve[i]]
    main_primes = [x for x in primes if 2 < x < 10_000]

    prime_pairs = set()
    prime_pair_map = {}
    for a, b in itertools.combinations(main_primes, 2):
        ab = int(f"{a}{b}")
        ba = int(f"{b}{a}")

        if is_prime_in_list(primes, ab) and is_prime_in_list(primes, ba):
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
        prime_index: int,
        state: list[int],
        state_index: int,
    ) -> Generator[list[int], None, None]:
    """
    Find prime pair set.
    """
    if state_index == len(state):
        yield state
        return

    i = prime_index
    while i < len(primes):
        p = primes[i]
        found = True
        for n in state[:state_index]:
            if (n, p) not in prime_pairs:
                found = False
                break

        if found:
            state[state_index] = p
            yield from find_prime_pair_set(prime_pairs, primes, i + 1, state, state_index + 1)

        i += 1


def solve_optimized() -> int:
    """
    search prime pair list
    """
    prime_sieve = gen_primes_sieve(10_000)
    main_primes = [x for x in range(3, 10_000, 2)
                   if is_prime_in_sieve(prime_sieve, x) and x % 5 != 0]
    prime_pairs = set()
    prime_pair_map = {}
    for a, b in itertools.combinations(main_primes, 2):
        ab = int(f"{a}{b}")
        ba = int(f"{b}{a}")

        if is_prime_in_list(main_primes, ab) and is_prime_in_list(main_primes, ba):
            prime_pairs.add((a, b))
            prime_pair_map.setdefault(a, set()).add(b)
            prime_pair_map.setdefault(b, set()).add(a)

    possible_primes = set()
    possible_prime_map = {}
    for k, v in prime_pair_map.items():
        if len(v) < TOTAL_NUMS - 1:
            continue

        possible_primes.add(k)
        l = []
        for x in v:
            if x in possible_primes:
                l.append(x)

        l.append(k)
        l.sort()
        possible_prime_map[k] = l

    possible_prime_list = list(possible_prime_map.keys())
    possible_prime_list.sort()

    state = [0] * TOTAL_NUMS
    for x in find_prime_pair_set(prime_pairs, possible_prime_list, 0, state, 0):
        return sum(x)

    return -1
