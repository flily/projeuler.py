#!/usr/bin/env python3
# coding: utf-8


"""
Integer Right Triangles

If p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, there are
exactly three solutions for p = 120. {20,48,52}, {24,45,51}, {30,40,50}

For which value of p ≤ 1000, is the number of solutions maximised?
"""


ANSWER = 840


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


def solve_order_generator() -> int:
    result, count = 0, 0
    for n in range(1, 1001):
        c = find_right_triangle_solutions_in_order(n)
        if c > count:
            result = n
            count = c

    return result


def find_right_triangle_solutions_by_euclid_formula(max_p: int) -> dict[int, int]:
    """
    Find the number of solutions for p.
    """
    result = {}
    for n in range(1, max_p // 2):
        for m in range(n + 1, max_p // n):
            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n
            p = a + b + c
            if p > max_p:
                break

            if a < b:
                a, b = b, a

            k = 1
            while k * p <= max_p:
                np = k * p
                if np not in result:
                    result[np] = set()

                result[np].add((k*a, k*b, k*c))
                k += 1

    return result

def solve_euclid_formula() -> int:
    results = find_right_triangle_solutions_by_euclid_formula(1000)
    result, count = 0, 0
    for p, solutions in results.items():
        c = len(solutions)
        if c > count:
            result = p
            count = c

    return result
