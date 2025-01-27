#!/usr/bin/env python3
# coding: utf-8


"""
Spiral Primes

Starting with 1 and spiralling anticlockwise in the following way, a square spiral with side length
7 is formed.

        [37]     36      35      34      33      32     [31]
         38     [17]     16      15      14     [13]     30
         39      18     [ 5]      4     [ 3]     12      29
         40      19       6       1       2      11      28
         41      20     [ 7]      8       9      10      27
         42      21      22      23      24      25      26
        [43]     44      45      46      47      48      49

It is interesting to note that the odd squares lie along the bottom right diagonal, but what is
more interesting is that 8 out of the 13 numbers lying along both diagonals are prime; that is, a
ratio of 8/13 ≈ 62%.

If one complete new layer is wrapped around the spiral above, a square spiral with side length 9
will be formed. If this process is continued, what is the side length of the square spiral for
which the ratio of primes along both diagonals first falls below 10%?
"""


from typing import Iterator


ANSWER = 26241

TIMEOUT_EXT = 1000.0


def is_prime(n: int) -> bool:
    """
    Check if n (positive) is a prime
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


def diagonal_generator() -> Iterator[int]:
    """
    Generate the diagonal numbers of the spiral
    """
    n = 1
    yield n
    d = 2
    c = 0
    while True:
        n += d
        c += 1
        yield n

        if c == 4:
            c = 0
            d += 2


def solve() -> int:
    primes, count = 0, 0
    for n in diagonal_generator():
        count += 1
        if is_prime(n):
            primes += 1

        if count > 1 and count % 4 == 1:
            if primes * 10 < count:
                break

    return (count + 1) // 2


def solve_skip_bottom_right() -> int:
    primes, count = 0, 0
    for n in diagonal_generator():
        count += 1
        c = count %4
        if c != 1 and is_prime(n):
            primes += 1

        if count > 1 and c == 1:
            if primes * 10 < count:
                break

    return (count + 1) // 2
