#!/usr/bin/env python3
# coding: utf-8


"""
Largest Exponential

Comparing two numbers written in index form like 2^11 and 3^7 is not difficult, as any calculator
would confirm that 2^11 = 2048 < 3^7 = 2187.

However, confirming that 632382^518061 > 519432^525806 would be much more difficult, as both
numbers contain over three million digits.

Using base_exp.txt (right click and 'Save Link/Target As...'), a 22K text file containing one
thousand lines with a base/exponent pair on each line, determine which line number has the greatest
numerical value.

NOTE: The first two lines in the file represent the numbers in the example given above.
"""


import math

from data import load


ANSWER = 709


def data_handler(data: str) -> list[tuple[int, int]]:
    result = []
    for line in data.splitlines():
        base_str, exp_str = line.split(",")
        result.append((int(base_str), int(exp_str)))

    return result


def solve() -> int:
    nums = load(data_handler)
    max_index = 0
    max_value = 0

    for i, (base, exp) in enumerate(nums):
        value = base ** exp
        if value > max_value:
            max_value = value
            max_index = i + 1

    return max_index


def solve_by_log() -> int:
    nums = load(data_handler)
    max_index = 0
    max_value = 0

    for i, (base, exp) in enumerate(nums):
        value = exp * math.log(base)
        if value > max_value:
            max_value = value
            max_index = i + 1

    return max_index
