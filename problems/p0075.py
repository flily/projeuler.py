#!/usr/bin/env python3
# coding: utf-8


"""
Singular Integer Right Triangles

It turns out that 12 cm is the smallest length of wire that can be bent to form an integer sided
right angle triangle in exactly one way, but there are many more examples.

    12 cm: (3,4,5)
    24 cm: (6,8,10)
    30 cm: (5,12,13)
    36 cm: (9,12,15)
    40 cm: (8,15,17)
    48 cm: (12,16,20)

In contrast, some lengths of wire, like 20 cm, cannot be bent to form an integer sided right angle
triangle, and other lengths allow more than one solution to be found; for example, using 120 cm
it is possible to form exactly three different integer sided right angle triangles.

    120 cm: (30,40,50), (20,48,52), (24,45,51)

Given that L is the length of the wire, for how many values of L <= 1_500_000 can exactly one
integer sided right angle triangle be formed?
"""


ANSWER = 161667
TIMEOUT_EXT = {
    "euclid_formula": 3000.0
}

LIMIT = 1_500_000


def find(l: int) -> int:
    count = 0
    for a in range(1, l // 2):
        for b in range(1, a):
            c = l - a - b
            if c < b:
                break

            if a * a + b * b == c * c:
                count += 1

    return count


def solve_naive() -> int:
    result = 0

    for l in range(1, LIMIT + 1):
        if find(l) == 1:
            result += 1

    return result


def solve_euclid_formula() -> int:
    solutions = {}
    for m in range(2, LIMIT // 3):
        for n in range(1, m):
            a = m * m - n * n
            b = 2 * m * n
            c = m * m + n * n
            length = a + b + c
            if length > LIMIT:
                break

            k = 1
            while k * length <= LIMIT:
                l = k * length
                if l not in solutions:
                    solutions[l] = set()

                sides = (min(k * a, k * b), max(k * a, k * b), k * c)
                solutions[l].add(sides)
                k += 1

    result = 0
    for _, elements in solutions.items():
        if len(elements) == 1:
            result += 1

    return result
