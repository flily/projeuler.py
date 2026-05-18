#!/usr/bin/env python3
# coding: utf-8


"""
Diophantine Equation

Consider quadratic Diophantine equations of the form:
    x^2 - Dy^2 = 1

For example, when D = 13 , the minimal solution in x is 649^2 - 13 * 180^2 = 1 .

It can be assumed that there are no solutions in positive integers when D is square.

By finding minimal solutions in x for D = {2, 3, 5, 6, 7} , we obtain the following:
    3^2 - 2 * 2^2 = 1
    2^2 - 3 * 1^2 = 1
    9^2 - 5 * 4^2 = 1
    5^2 - 6 * 2^2 = 1
    8^2 - 7 * 3^2 = 1

Hence, by considering minimal solutions in x for D <= 7 , the largest x is obtained when D = 5 .

Find the value of D <= 1000 in minimal solutions of x for which the largest value of x is obtained.
"""


ANSWER = 661


def find_minimal_solution(d: int) -> tuple[int, int]:
    y = 1
    while True:
        x2 = y * y * d + 1
        x = int(x2 ** 0.5)
        if x * x == x2:
            return x, y

        y += 1

# When D=109, x=158_070_671_986_249 and y=15_140_424_455_100
# It is impossible to find by brute-force.
def solve() -> int:
    squares = set(i * i for i in range(1, 32))
    result = 0
    index = 0

    for d in range(1, 1001):
        if d in squares:
            continue

        rx, _ = find_minimal_solution(d)
        if rx > result:
            result = rx
            index = d

    return index

def get_pell_equation(d: int) -> tuple[int, int]:
    """
    Solve Pell's equation x^2 - Dy^2 = 1 for given D.
    """
    m, dd, a0 = 0, 1, int(d**0.5)
    a1 = a0
    x1, x0 = 1, a1
    y1, y0 = 0, 1
    while x0 * x0 - d * y0 * y0 != 1:
        m = dd * a1 - m
        dd = (d - m * m) // dd
        a1 = (a0 + m) // dd

        x1, x0 = x0, a1 * x0 + x1
        y1, y0 = y0, a1 * y0 + y1

    return x0, y0


def solve_with_formula() -> int:
    result = 0
    index = 0

    for d in range(1, 1001):
        if int(d**0.5)**2 == d:
            continue

        x, _ = get_pell_equation(d)
        if x > result:
            result = x
            index = d

    return index
