#!/usr/bin/env python3
# coding: utf-8


"""
Maximum Path Sum II

By starting at the top of the triangle below and moving to adjacent numbers on the row below, the
maximum total from top to bottom is 23.

                [3]
            [7]     4
        2       [4]     6
    8       5       [9]     3

That is, 3 + 7 + 4 + 9 = 23.

Find the maximum total from top to bottom in triangle.txt (right click and 'Save Link/Target As...'
), a 15K text file containing a triangle with one-hundred rows.

NOTE: This is a much more difficult version of Problem 18. It is not possible to try every route to
solve this problem, as there are 2^99 altogether! If you could check one trillion (10^12) routes
every second it would take over twenty billion years to check them all. There is an efficient
algorithm to solve it. ;o)
"""


from data.p0067 import load


PID = 67
ANSWER = 7273


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
    return max_path_sum_recursive(load(), 0, 0, 0)


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
    return path_sum_flood(load())
