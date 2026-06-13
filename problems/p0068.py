#!/usr/bin/env python3
# coding: utf-8


"""
Magic 5-gon Ring

Consider the following "magic" 3-gon ring, filled with the numbers 1 to 6, and each line adding
to nine.

            4
              \
                3
              /   \
            1  ---  2  ---  6
           /
        5

Working clockwise, and starting from the group of three with the numerically lowest external
node (4,3,2 in this example), each solution can be described uniquely. For example, the above
solution can be described by the set: 4,3,2; 6,2,1; 5,1,3.

It is possible to complete the ring with four different totals: 9, 10, 11, and 12. There are eight
solutions in total.

    Total       Solution Set
      9         4,2,3; 5,3,1; 6,1,2
      9	        4,3,2; 6,2,1; 5,1,3
     10         2,3,5; 4,5,1; 6,1,3
     10         2,5,3; 6,3,1; 4,1,5
     11         1,4,6; 3,6,2; 5,2,4
     11         1,6,4; 5,4,2; 3,2,6
     12         1,5,6; 2,6,4; 3,4,5
     12         1,6,5; 3,5,4; 2,4,6

By concatenating each group it is possible to form 9-digit strings; the maximum string for a 3-gon
ring is 432621513.

Using the numbers 1 to 10, and depending on arrangements, it is possible to form 16- and 17-digit
strings. What is the maximum 16-digit string for a "magic" 5-gon ring?
"""


import itertools


ANSWER = 6531031914842725
TIMEOUT_EXT = 1000.0


def gon_flags(inner: list[int], outer: list[int]) -> int:
    s = []
    l = len(inner)
    for i in range(l):
        n1 = outer[i]
        n2 = inner[i]
        n3 = inner[(i + 1) % l]
        s.append(f"{n1}{n2}{n3}")

    return int("".join(s))


def check_gon(inner: list[int], outer: list[int]) -> int:
    s = 0
    l = len(inner)
    for i in range(l):
        si = outer[i] + inner[i] + inner[(i + 1) % l]
        if s == 0:
            s = si
        else:
            if s != si:
                return 0

    return s


MIN_17 = 10_000_000_000_000_000

def solve() -> int:
    size = 5
    digits = range(1, (2 * size) + 1)
    max_flag = 0
    for x in itertools.permutations(digits, size * 2):
        inner = list(x[:size])
        outer = list(x[size:])
        if outer[0] != min(outer):
            continue

        g = check_gon(inner, outer)
        if g > 0:
            flag = gon_flags(inner, outer)
            if flag > MIN_17:
                continue

            max_flag = max(max_flag, flag)

    return max_flag


def gon_flags_one(size: int, x: list[int]) -> int:
    s = []
    for i in range(size):
        n1 = x[size + i]
        n2 = x[i]
        n3 = x[(i + 1) % size]
        s.append(f"{n1}{n2}{n3}")

    return int("".join(s))


def check_gon_one(size: int, x: list[int]) -> int:
    s = 0
    for i in range(size):
        si = x[size + i] + x[i] + x[(i + 1) % size]
        if s == 0:
            s = si
        else:
            if s != si:
                return 0

    return s


def solve_one_list() -> int:
    size = 5
    digits = range(1, (2 * size) + 1)
    max_flag = 0
    for x in itertools.permutations(digits, size * 2):
        valid = True
        for i in range(size - 1):
            if x[size] > x[size + 1 + i]:
                valid = False
                break

        if not valid:
            continue

        g = check_gon_one(size, x)
        if g > 0:
            flag = gon_flags_one(size, x)
            if flag > MIN_17:
                continue

            max_flag = max(max_flag, flag)

    return max_flag
