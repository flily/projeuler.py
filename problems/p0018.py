#!/usr/bin/env python3
# coding: utf-8


"""
Maximum Path Sum I

By starting at the top of the triangle below and moving to adjacent numbers on the row below, the
maximum total from top to bottom is 23.

                [3]
            [7]     4
        2       [4]     6
    8       5       [9]     3

That is, 3 + 7 + 4 + 9 = 23.

Find the maximum total from top to bottom of the triangle below:

75
95 64
17 47 82
18 35 87 10
20 04 82 47 65
19 01 23 75 03 34
88 02 77 73 07 63 67
99 65 04 28 06 16 70 92
41 41 26 56 83 40 80 70 33
41 48 72 33 47 32 37 16 94 29
53 71 44 65 25 43 91 52 97 51 14
70 11 33 28 77 73 17 78 39 68 17 57
91 71 52 38 17 14 91 43 58 50 27 29 48
63 66 04 68 89 53 67 30 73 16 69 87 40 31
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23

NOTE: As there are only 16384 routes, it is possible to solve this problem by trying every route.
However, Problem 67, is the same challenge with a triangle containing one-hundred rows; it cannot be
solved by brute force, and requires a clever method! ;o)
"""


PID = 18
ANSWER = 1074


TRIANGLE = [
    [75],
    [95, 64],
    [17, 47, 82],
    [18, 35, 87, 10],
    [20,  4, 82, 47, 65],
    [19,  1, 23, 75,  3, 34],
    [88,  2, 77, 73,  7, 63, 67],
    [99, 65,  4, 28,  6, 16, 70, 92],
    [41, 41, 26, 56, 83, 40, 80, 70, 33],
    [41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
    [53, 71, 44, 65, 25, 43, 91, 52, 97, 51, 14],
    [70, 11, 33, 28, 77, 73, 17, 78, 39, 68, 17, 57],
    [91, 71, 52, 38, 17, 14, 91, 43, 58, 50, 27, 29, 48],
    [63, 66,  4, 68, 89, 53, 67, 30, 73, 16, 69, 87, 40, 31],
    [4,  62, 98, 27, 23,  9, 70, 98, 73, 93, 38, 53, 60,  4, 23],
]


def max_path_sum_recursive(triangle, row: int, column: int, s: int):
    """
    Get the path sum from the given row and column.
    """
    current = triangle[row][column]

    if row >= len(triangle) - 1:
        return s + current

    left = max_path_sum_recursive(triangle, row + 1, column, s + current)
    right = max_path_sum_recursive(triangle, row + 1, column + 1, s + current)
    return max(left, right)


def solve_brute_force() -> int:
    return max_path_sum_recursive(TRIANGLE, 0, 0, 0)


def path_sum_flood(triangle) -> int:
    """
    Get the path sum.
    """
    result = triangle[0]
    for x in range(1, len(triangle)):
        row = triangle[x]
        new_row = [0] * (len(row))
        for i, v in enumerate(row):
            left = result[i - 1] if i > 0 else 0
            right = result[i] if i < len(result) else 0
            new_row[i] = max(left, right) + v
        result = new_row

    return max(result)


def solve_flood() -> int:
    return path_sum_flood(TRIANGLE)
