# coding: utf-8
#!/usr/bin/env python3


"""
Almost Equilateral Triangles

It is easily proved that no equilateral triangle exists with integral length sides and integral
area. However, the almost equilateral triangle 5-5-6 has an area of 12 square units.

We shall define an almost equilateral triangle to be a triangle for which two sides are equal and
the third differs by no more than one unit.

Find the sum of the perimeters of all almost equilateral triangles with integral side lengths
and area and whose perimeters do not exceed one billion (1_000_000_000).
"""


import math

from typing import Iterable


ANSWER = 518408346

LIMIT = 1_000_000_000


def check_almost_equilateral_isqrt(a: int, b: int, c: int) -> int:
    s = (a + b + c) // 2
    d = s * (s - a) * (s - b) * (s - c)
    area = math.isqrt(d)
    if area * area != d:
        return 0

    return area


# checked, get correct answer, but too slow, cost about 130s in python3.14
# and pypy3 cost about 145s.
def solve_naive_isqrt() -> int:
    """
    Naive with math.isqrt
    """
    result = 0
    for x in range(3, LIMIT // 3 + 1, 2):
        s1 = check_almost_equilateral_isqrt(x, x, x - 1)
        if s1 > 0:
            # print(f"(-) found ({x}, {x}, {x - 1}), area = {s1}, perimeter = {3 * x - 1}")
            result += (3 * x) - 1

        s2 = check_almost_equilateral_isqrt(x, x, x + 1)
        if s2 > 0:
            # print(f"(+) found ({x}, {x}, {x + 1}), area = {s2}, perimeter = {3 * x + 1}")
            result += (3 * x) + 1

    return result


def check_almost_equilateral_sqrt_int(a: int, b: int, c: int) -> int:
    s = (a + b + c) // 2
    d = s * (s - a) * (s - b) * (s - c)
    area = int(math.sqrt(d))
    if area * area != d:
        return 0

    return area


def solve_naive_sqrt() -> int:
    """
    Naive with int(n ** 0.5)
    """
    result = 0
    for x in range(3, LIMIT // 3 + 1, 2):
        s1 = check_almost_equilateral_sqrt_int(x, x, x - 1)
        if s1 > 0:
            # print(f"(-) found ({x}, {x}, {x - 1}), area = {s1}, perimeter = {3 * x - 1}")
            result += (3 * x) - 1

        s2 = check_almost_equilateral_sqrt_int(x, x, x + 1)
        if s2 > 0:
            # print(f"(+) found ({x}, {x}, {x + 1}), area = {s2}, perimeter = {3 * x + 1}")
            result += (3 * x) + 1

    return result


def seq_add(limit: int) -> Iterable[int]:
    a, b = 1, 5
    while b < limit:
        yield b
        a, b = b, 14 * b - a - 4

def seq_sub(limit: int) -> Iterable[int]:
    a, b = 1, 17
    while b < limit:
        yield b
        a, b = b, 14 * b - a + 4


# use naive_sqrt, easy to found two sequences of (x, x, x - 1) and (x, x, x + 1)
#             [0]       1       2       3       4       5           a{n}
# (x + 1)     [1]       5      65     901    3361   12545   14*a{n-1} - a{n-2} - 4
# (x - 1)     [1]      17     241    3361   46817  652081   14*a{n-1} - a{n-2} + 4
def solve_formula() -> int:
    result = 0

    for x in seq_add(LIMIT // 3):
        result += (3 * x) + 1

    for x in seq_sub(LIMIT // 3):
        result += (3 * x) - 1

    return result
