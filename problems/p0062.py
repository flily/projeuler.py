#!/usr/bin/env python3
# coding: utf-8


"""
Cubic Permutations

The cube, 41063625 (345^3), can be permuted to produce two other cubes: 56623104 (384^3) and
66430125 (405^3). In fact, 41063625 is the smallest cube which has exactly three permutations of
its digits which are also cube.

Find the smallest cube for which exactly five permutations of its digits are cube.
"""


ANSWER = 127035954683


def solve() -> int:
    """
    Solve the problem.
    """
    digit_map = {}

    for x in range(1, 10000):
        cube = x ** 3
        key = "".join(sorted(str(cube)))
        if key not in digit_map:
            digit_map[key] = [cube]
        else:
            digit_map[key].append(cube)
            if len(digit_map[key]) == 5:
                return digit_map[key][0]

    return 0
