#!/usr/bin/env python3
# coding: utf-8


"""
Path Sum: Three Ways

NOTE: This problem is a more challenging version of Problem 81.

The minimal path sum in the 5 by 5 matrix below, by starting in any cell in the left column and
finishing in any cell in the right column, and only moving up, down, and right, is indicated
in red and bold; the sum is equal to 994.

        |  131   673  [234] [103] [ 18] |
        | [201] [ 96] [342]  965   150  |
        |  630   803   746   422   111  |
        |  537   699   497   121   956  |
        |  805   732   524    37   331  |

Find the minimal path sum from the left column to the right column in matrix.txt
(right click and "Save Link/Target As..."), a 31K text file containing an 80 by 80 matrix.
"""


from data import load


ANSWER = 260324

EXAMPLE = [
    [131, 673, 234, 103,  18],
    [201,  96, 342, 965, 150],
    [630, 803, 746, 422, 111],
    [537, 699, 497, 121, 956],
    [805, 732, 524,  37, 331],
]


def data_handler(raw: str) -> list[list[int]]:
    result = []

    for line in raw.splitlines():
        row = [int(x) for x in line.split(",")]
        result.append(row)

    return result


def update_cell(
    matrix: list[list[int]], size: tuple[int, int], path: list[list[int]], position: tuple[int, int]
) -> None:
    width, height = size
    row, col = position
    del width

    current = matrix[row][col]
    neighbors = []

    if col == 0:
        neighbors.append(current)

    if row > 0:
        upper = path[row - 1][col]
        if upper is not None:
            neighbors.append(upper + current)

    if row < height - 1:
        lower = path[row + 1][col]
        if lower is not None:
            neighbors.append(lower + current)

    if col > 0:
        left = path[row][col - 1]
        if left is not None:
            neighbors.append(left + current)

    path[row][col] = min(neighbors)


def search_minimal_path_sum_flood(matrix: list[list[int]], size: tuple[int, int]) -> list[int]:
    width, height = size
    path = [[None] * width for _ in range(height)]

    for x in range(height):
        path[x][0] = matrix[x][0]

    for x in range(width):
        for y in range(height):
            update_cell(matrix, size, path, (y, x))

        for y in range(height - 1, -1, -1):
            update_cell(matrix, size, path, (y, x))

        # for row in path:
        #     items = [f"{x or -1:>5}" for x in row]
        #     print("  ".join(items))
        # print("--------")

    return min(path[y][width - 1] for y in range(height))

def solve_bruteforce_breadth_first_flood() -> int:
    """
    brute force, breadth first, flood
    """
    raw = load(data_handler)
    # raw = EXAMPLE

    size = len(raw)     # square matrix
    result = search_minimal_path_sum_flood(raw, (size, size))

    return result
