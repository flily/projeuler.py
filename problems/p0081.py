#!/usr/bin/env python3
# coding: utf-8


"""
Path Sum: Two Ways

In the 5 by 5 matrix below, the minimal path sum from the top left to the bottom right, by
**only moving to the right and down**, is indicated in bold red and is equal to 2427.

        | [131]  673   234   103    18  |
        | [201] [ 96] [342]  965   150  |
        |  630   803  [746] [422]  111  |
        |  537   699   497  [121]  956  |
        |  805   732   524  [ 37] [331] |

Find the minimal path sum from the top left to the bottom right by only moving right and down in
matrix.txt (right click and "Save Link/Target As..."), a 31K text file containing
an 80 by 80 matrix.
"""


from data import load


ANSWER = 427337

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


def search_minimal_path_sum_dfs(
    matrix: list[list[int]], size: tuple[int, int], position: tuple[int, int], s: int
) -> list[int]:
    width, height = size
    row, col = position

    current = matrix[row][col]
    next_sum = s + current
    if col < width - 1:
        result_right = search_minimal_path_sum_dfs(matrix, size, (row, col + 1), next_sum)
    else:
        result_right = None

    if row < height - 1:
        result_down = search_minimal_path_sum_dfs(matrix, size, (row + 1, col), next_sum)
    else:
        result_down = None

    if result_right is None and result_down is None:
        result = next_sum

    elif result_right is None:
        result = result_down

    elif result_down is None:
        result = result_right

    else:
        if result_right < result_down:
            result = result_right
        else:
            result = result_down

    return result

# checked on example, correct
def solve_bruteforce_depth_first() -> int:
    """
    brute force, depth first search
    """
    raw = load(data_handler)
    # raw = EXAMPLE

    # height, width = len(raw), len(raw[0])
    size = len(raw)     # square matrix
    for x in range(1, size +1):
        result = search_minimal_path_sum_dfs(raw, (81 - x, x), (0, 0), 0)
        # print(f"size: ({81 - x}, {x}), result: {result}")

    return result


def update_cell(
    matrix: list[list[int]], size: tuple[int, int], path: list[list[int]], position: tuple[int, int]
) -> None:
    width, height = size
    row, col = position
    del width, height

    current = matrix[row][col]
    neighbors = []

    if row == 0 and col == 0:
        neighbors.append(current)

    if row > 0:
        upper = path[row - 1][col]
        if upper is not None:
            neighbors.append(upper + current)

    if col > 0:
        left = path[row][col - 1]
        if left is not None:
            neighbors.append(left + current)

    path[row][col] = min(neighbors)


def search_minimal_path_sum_flood(matrix: list[list[int]], size: tuple[int, int]) -> list[int]:
    width, height = size
    path = [[None] * width for _ in range(height)]

    path[0][0] = matrix[0][0]
    for i in range(width + height):
        for x in range(i + 1):
            y = i - x
            if x < width and y < height:
                update_cell(matrix, size, path, (y, x))

    # for row in path:
    #     items = [f"{x or -1:>5}" for x in row]
    #     print("  ".join(items))

    return path[height - 1][width - 1]

def solve_bruteforce_breadth_first_flood() -> int:
    """
    brute force, breadth first, flood
    """
    raw = load(data_handler)
    # raw = EXAMPLE

    size = len(raw)     # square matrix
    result = search_minimal_path_sum_flood(raw, (size, size))

    return result


def search_minimal_path_sum_bfs_mark(matrix: list[list[int]], size: tuple[int, int]) -> list[int]:
    width, height = size
    path = [[None] * width for _ in range(height)]
    path[0][0] = matrix[0][0]

    queue = [(0, 0)]
    queue_count = {
        (0, 0): 1
    }

    while queue:
        x, y = queue.pop(0)
        update_cell(matrix, size, path, (y, x))
        queue_count[(x, y)] -= 1

        if x + 1 < width:
            # update right
            c = queue_count.get((x + 1, y), 0)
            if c <= 0:
                queue.append((x + 1, y))
                queue_count[(x + 1, y)] = c + 1

        if y + 1 < height:
            # update down
            c = queue_count.get((x, y + 1), 0)
            if c <= 0:
                queue.append((x, y + 1))
                queue_count[(x, y + 1)] = c + 1

    # for row in path:
    #     items = [f"{x or -1:>5}" for x in row]
    #     print("  ".join(items))

    return path[height - 1][width - 1]

def solve_bruteforce_breadth_first_mark() -> int:
    """
    brute force, breadth first, mark
    """
    raw = load(data_handler)
    # raw = EXAMPLE

    size = len(raw)     # square matrix
    result = search_minimal_path_sum_bfs_mark(raw, (size, size))

    return result
