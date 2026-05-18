#!/usr/bin/env python3
# coding: utf-8


"""
Convergents of e

The square root of  can be written as an infinite continued fraction.
    sqrt(2) = 1 + (1 / (2 + (1 / (2 + (1 / (2 + ...))))))

The infinite continued fraction can be written, sqrt(2) = [1;(2)], (2) indicates that 2 repeats
ad infinitum. In a similar way, sqrt(23) = [4;(1, 3, 1, 8)].

It turns out that the sequence of partial values of continued fractions for square roots provide
the best rational approximations. Let us consider the convergents for sqrt(2).
    1 + (1 / 2)                                     = 3/2
    1 + (1 / (2 + (1 / 2)))                         = 7/5
    1 + (1 / (2 + (1 / (2 + (1 / 2)))))             = 17/12
    1 + (1 / (2 + (1 / (2 + (1 / (2 + (1 / 2))))))) = 41/29

Hence the sequence of the first ten convergents for sqrt(2) are:
    1, 3/2, 7/5, 17/12, 41/29, 99/70, 239/169, 577/408, 1393/985, 3363/2378, ...

What is most surprising is that the important mathematical constant,
    e = [2; 1, 2, 1, 1, 4, 1, 1, 6, ..., 1, 2k, 1, ...]

The first ten terms in the sequence of convergents for e are:
    2, 3, 8/3, 11/4, 19/7, 87/32, 106/39, 193/71, 1261/461, 1457/536, ...

The sum of digits in the numerator of the 10th convergent is 1 + 4 + 5 + 7 = 17.

Find the sum of digits in the numerator of the 100th convergent of the continued fraction for e.
"""


ANSWER = 272


def calculate_convergent(start, terms, n):
    if n <= 1:
        return start, 1

    d, f = 1, terms(n)
    for i in range(n - 1, 1, -1):
        k = terms(i)
        d, f = f, f * k + d

    d += start * f
    return d, f


def e_index(n):
    if (n - 1) % 3 == 2:
        return 2 * (((n - 1) // 3) + 1)
    else:
        return 1


def digits_sum(n):
    s = 0
    while n > 0:
        s += n % 10
        n //= 10
    return s


def solve() -> int:
    d, _ = calculate_convergent(2, e_index, 100)
    return digits_sum(d)
