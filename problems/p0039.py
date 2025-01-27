#!/usr/bin/env python3
# coding: utf-8


"""
Integer Right Triangles

If p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, there are
exactly three solutions for p = 120. {20,48,52}, {24,45,51}, {30,40,50}

For which value of p ≤ 1000, is the number of solutions maximised?
"""


ANSWER = 840
TIMEOUT_EXT = 5000.0


def can_be_right_triangle(a: int, b: int, c: int) -> bool:
    """
    Return True if a, b, c can be the sides of a right triangle.
    """
    aa = a * a
    bb = b * b
    cc = c * c

    return aa + bb == cc or aa + cc == bb or bb + cc == aa


def find_right_triangle_solutions_naive(p: int) -> int:
    """
    Find the number of solutions for p.
    """
    result = 0
    for a in range(1, p):
        for b in range(1, p):
            c = p - a - b
            if c <= 0:
                break

            if can_be_right_triangle(a, b, c):
                result += 1

    return result


def solve_naive() -> int:
    result, count = 0, 0
    for n in range(1, 1001):
        c = find_right_triangle_solutions_naive(n)
        if c > count:
            result = n
            count = c

    return result


def can_be_right_triangle_in_order(a: int, b: int, c: int) -> bool:
    """
    Return True if a, b, c can be the sides of a right triangle.
    """
    aa = a * a
    bb = b * b
    cc = c * c

    return aa + bb == cc


def find_right_triangle_solutions_in_order(p: int) -> int:
    """
    Find the number of solutions for p.
    """
    result = 0
    for a in range(1, p // 2):
        for b in range(a, (p - a) // 2):
            c = p - a - b
            if c <= 0:
                break

            if can_be_right_triangle(a, b, c):
                result += 1

    return result


def solve_in_order_generator() -> int:
    result, count = 0, 0
    for n in range(1, 1001):
        c = find_right_triangle_solutions_in_order(n)
        if c > count:
            result = n
            count = c

    return result
