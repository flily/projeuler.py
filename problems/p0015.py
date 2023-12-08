#!/usr/bin/env python3
# coding: utf-8


"""
Lattice Paths

Starting in the top left corner of a 2 x 2 grid, and only being able to move to the right and down,
there are exactly 6 routes to the bottom right corner.

    * == * == *    * == * -- *    * == * -- *
    |    |    ||   |    ||   |    |    ||   |
    * -- * -- *    * -- * == *    * -- * -- *
    |    |    ||   |    |    ||   |    ||   |
    * -- * -- *    * -- * -- *    * -- * == *

    * -- * -- *    * -- * -- *    * -- * -- *
    ||   |    |    ||   |    |    ||   |    |
    * == * == *    * == * -- *    * -- * -- *
    |    |    ||   |    ||   |    ||   |    |
    * -- * -- *    * -- * == *    * == * == *


How many such routes are there through a 20 x 20 grid?
"""


PID = 15
ANSWER = 137846528820


def calc_lattice_paths(width: int, height: int) -> int:
    """
    Calculate the number of lattice paths through a grid of the given width and height.
    """
    row = [1] * width
    for _ in range(height - 1):
        for i in range(1, width):
            row[i] += row[i - 1]

    return row[-1]


def solve() -> int:
    return calc_lattice_paths(20 + 1, 20 + 1)
