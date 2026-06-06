#!/usr/bin/env python3
# coding: utf-8


"""
Counting Rectangles

By counting carefully it can be seen that a rectangular grid measuring 3 by 2 contains
eighteen rectangles:


Although there exists no rectangular grid that contains exactly two million rectangles, find
the area of the grid with the nearest solution.
"""


ANSWER = 2772

TARGET = 2_000_000


def calculate_rectangles(width: int, height: int) -> int:
    s = 0
    for i in range(1, width + 1):
        for j in range(1, height + 1):
            s += (width - i + 1) * (height - j + 1)

    return s


def solve() -> int:
    size = (0, 0)
    min_diff = TARGET

    for w in range(1, 100):
        for h in range(w, 100):
            p = calculate_rectangles(w, h)
            diff = abs(p - TARGET)
            if diff < min_diff:
                min_diff = diff
                size = (w, h)

    return size[0] * size[1]


#      1   2   3   4   5
# 1:   1   3   6  10  15
# 2:   3   9  18  30  45
# 3:   6  18  36  60  90
# 4:  10  30  60 100 150
# 5:  15  45  90 150 225
def calculate_rectangles_formula(width: int, height: int) -> int:
    w = width * (width + 1) // 2
    h = height * (height + 1) // 2
    return w * h

def solve_formula() -> int:
    size = (0, 0)
    min_diff = TARGET

    for w in range(100):
        for h in range(w, 100):
            p = calculate_rectangles_formula(w, h)
            diff = abs(p - TARGET)
            if diff < min_diff:
                min_diff = diff
                size = (w, h)

    return size[0] * size[1]
