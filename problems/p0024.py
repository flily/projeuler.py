#!/usr/bin/env python3
# coding: utf-8


"""
Lexicographic Permutations

A permutation is an ordered arrangement of objects. For example, 3124 is one possible permutation
of the digits 1, 2, 3 and 4. If all of the permutations are listed numerically or alphabetically,
we call it lexicographic order. The lexicographic permutations of 0, 1 and 2 are:

            012   021   102   120   201   210

What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?
"""


from typing import Iterable


PID = 24
ANSWER = 2783915460


def generate_permutations(
    digits: Iterable[bool],
    got: Iterable[int] = None,
    i: int = 0,
    count: int = 0,
    stop_at: int = None,
) -> (int, int):
    """
    Generate permutations of digits.
    """
    if i >= len(digits):
        v = 0
        c = count + 1
        if stop_at is not None and c >= stop_at:
            v = int("".join(str(x) for x in got))

        return c, v

    if not got:
        got = [None] * len(digits)

    j = 0
    found_count = count
    while j < len(digits):
        if not digits[j]:
            digits[j] = True
            got[i] = j
            c, value = generate_permutations(digits, got, i + 1, found_count, stop_at)
            got[i] = None
            digits[j] = False
            found_count = c
            if value > 0:
                return c, value

        j += 1

    return found_count, 0


def solve_naive() -> int:
    nums = [False] * 10
    _, value = generate_permutations(nums, stop_at=1_000_000)
    return value


def factorial(n: int) -> int:
    """
    Get the factorial of n.
    """
    if n == 0:
        return 1

    result = n
    for i in range(2, n):
        result *= i

    return result


def solve_in_math() -> int:
    digits_left = 9
    numbers_left = 1_000_000 - 1
    digits_use = [False] * 10
    digits_pick = []

    while digits_left >= 0:
        block_count = factorial(digits_left)
        number_index = numbers_left // block_count

        i, j = 0, 0
        while i < len(digits_use):
            if not digits_use[i]:
                if j == number_index:
                    digits_use[i] = True
                    digits_pick.append(i)
                    break

                j += 1
            i += 1

        numbers_left -= number_index * block_count
        digits_left -= 1

    return int("".join(str(x) for x in digits_pick))
