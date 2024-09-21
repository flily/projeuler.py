#!/usr/bin/env python3
# coding: utf-8


"""
Pandigital Multiples

Take the number 192 and multiply it by each of 1, 2, and 3:
        192 × 1 = 192
        192 × 2 = 384
        192 × 3 = 576

By concatenating each product we get the 1 to 9 pandigital, 192384576. We will call 192384576 the
concatenated product of 192 and (1,2,3).

The same can be achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5, giving the
pandigital, 918273645, which is the concatenated product of 9 and (1,2,3,4,5).

What is the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated product
of an integer with (1,2, ... , n) where n > 1?
"""


import math


ANSWER = 932718654


def is_pandigital_9(n: int) -> bool:
    """
    Check if n is a 9-digit pandigital number.
    """
    if n < 123456789 or n > 987654321:
        return False

    digits = [False] * 10
    while n > 0:
        d = n % 10
        if d == 0 or digits[d]:
            return False

        digits[d] = True
        n //= 10

    return True


def concatencated_product(*nums: int) -> int:
    """
    Return the concatenated product of nums.
    """
    size = 0
    for n in nums:
        size += math.floor(math.log10(n)) + 1

    result = 0
    left = size
    for n in nums:
        left -= math.floor(math.log10(n)) + 1
        result += n * (10 ** left)

    return result


def solve_naive() -> int:
    result = 0
    for n in range(10, 10000):
        digits = 0
        nums = []
        for i in range(1, 10):
            d = n * i
            digits += math.floor(math.log10(d)) + 1
            # print(f"  - {n} x {i} = {d}  digits: {digits}")
            nums.append(d)
            if digits >= 9:
                break

        if digits == 9:
            p = concatencated_product(*nums)
            if is_pandigital_9(p):
                result = max(result, p)

    return result
