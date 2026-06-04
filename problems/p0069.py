#!/usr/bin/env python3
# coding: utf-8


"""
Totient Maximum

Euler's totient function, Φ(n) [sometimes called the phi function], is defined as the number of
positive integers not exceeding n which are relatively prime to n. For example, as 1, 2, 4, 5, 7,
and 8 are all less than or equal to nine and relatively prime to nine, Φ(9) = 6.

+----+--------------------+------+--------+
|  n |  Relatively Prime  | Φ(n) | n/Φ(n) |
+----+--------------------+------+--------+
|  2 | 1                  | 1    | 2      |
|  3 | 1,2                | 2    | 1.5    |
|  4 | 1,3                | 2    | 2      |
|  5 | 1,2,3,4            | 4    | 1.25   |
|  6 | 1,5                | 2    | 3      |
|  7 | 1,2,3,4,5,6        | 6    | 1.1666 |
|  8 | 1,3,5,7            | 4    | 2      |
|  9 | 1,2,4,5,7,8        | 6    | 1.5    |
| 10 | 1,3,7,9            | 4    | 2.5    |
+----+--------------------+------+--------+


It can be seen that n = 6 produces a maximum n/Φ(n) for n ≤ 10.

Find the value of n ≤ 1,000,000 for which n/Φ(n) is a maximum.
"""


import math


ANSWER = 510510


LIMIT = 1_000_000


def relative_prime(n: int) -> int:
    """
    Get the count of numbers that are relatively prime to n.
    """
    count = 0
    for i in range(1, n):
        if math.gcd(i, n) == 1:
            count += 1

    return count


def nphi(n: int) -> float:
    """
    Get the value of Φ(n).
    """
    rp = relative_prime(n)
    # print(f"n: {n}, Φ(n): {len(rp)}, relatively prime: {rp}")
    return n / rp


def solve_naive() -> int:
    result = 0
    max_nphi = 0.0
    for n in range(2, LIMIT + 1):
        np = nphi(n)
        if np > max_nphi:
            max_nphi = np
            result = n
            # print(f"found new max n/Φ(n): {result} with n/Φ(n) = {max_nphi}")

    return result


def nphi_limit(n: int, max_nphi: float) -> float:
    """
    Get the value of n/Φ(n) for n.
    """
    count = 0
    for i in range(1, n, 2):
        if math.gcd(i, n) == 1:
            count += 1

        if i > 300 and i / count < max_nphi:
            return 0.0

    for i in range(2, n, 2):
        if math.gcd(i, n) == 1:
            count += 1

    return n / count


def solve_with_limit() -> int:
    """
    limit n/Φ(n) with max_nphi
    """
    result = 0
    max_nphi = 0.0
    for n in range(2, LIMIT + 1):
        np = nphi_limit(n, max_nphi)
        if np > max_nphi:
            max_nphi = np
            result = n

    return result


def sieve_totient(max_num: int) -> int:
    """
    Get the value of n/Φ(n) for n using sieve.
    """
    sieve = [0.0] * (max_num + 1)
    max_nphi = 0.0
    result = 0

    for i in range(2, max_num + 1):
        if sieve[i] < 0.1:
            for j in range(i, max_num + 1, i):
                if sieve[j] < 0.1:
                    sieve[j] = j * (i - 1) // i
                else:
                    sieve[j] = sieve[j] * (i - 1) // i
        else:
            np = float(i) / sieve[i]
            if np > max_nphi:
                max_nphi = np
                result = i

    return result


def solve_with_sieve() -> int:
    """
    generate with sieve
    """
    result = sieve_totient(LIMIT)
    return result
