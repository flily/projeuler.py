#!/usr/bin/env python3
# coding: utf-8


"""
Square Root Digital Expansion

It is well known that if the square root of a natural number is not an integer, then it is
irrational. The decimal expansion of such square roots is infinite without any repeating pattern
at all.

The square root of two is 1.41421356237309504880..., and the digital sum of the first one hundred
decimal digits is 475.

For the first one hundred natural numbers, find the total of the digital sums of the first
one hundred decimal digits for all the irrational square roots.
"""


ANSWER = 40886


def square_root_digits(n: int, limit: int) -> tuple[int, list[int]]:
    a = 1
    while a * a <= n:
        a += 1

    a -= 1
    remain = n - a * a
    if remain == 0:
        return a, []

    # print(f"a={a}, remain={remain}")
    digits = []
    base = a + a
    while len(digits) < limit:
        base *= 10
        remain *= 100
        d = 1
        while (base + d) * d < remain:
            d += 1

        d -= 1
        # print(f"{base+d:>5}x{d:>1} | {remain:>8}")
        # print(f"{'':>7} | {(base + d) * d:>8}")
        # print("--------")
        digits.append(d)
        remain -= (base + d) * d
        base += 2 * d

    return a, digits

def solve() -> int:
    result = 0
    for n in range(1, 101):
        n, digits = square_root_digits(n, 99)
        if digits:
            result += n + sum(digits)

    return result
