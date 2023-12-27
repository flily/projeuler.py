#!/usr/bin/env python3
# coding: utf-8


"""
Pandigital Products

We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly
once; for example, the 5-digit number, 15234, is 1 through 5 pandigital.

The product 7254 is unusual, as the identity, 39 × 186 = 7254, containing multiplicand, multiplier,
and product is 1 through 9 pandigital.

Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1
through 9 pandigital.

HINT: Some products can be obtained in more than one way so be sure to only include it once in your
sum.
"""


ANSWER = 45228


def check_pandigital(*nums: int) -> bool:
    """
    Check if numbers are pandigital.
    """
    digits = [False] * 10
    for num in nums:
        if num == 0:
            return False

        while num > 0:
            digit = num % 10
            if digit == 0:
                return False

            if digits[digit]:
                return False

            digits[digit] = True
            num //= 10

    for i in range(1, 10):
        if not digits[i]:
            return False

    return True


def solve_naive() -> int:
    result = set()
    for a in range(1000):
        for b in range(a, 10000):
            c = a * b
            if check_pandigital(a, b, c):
                result.add(c)

    return sum(result)


def can_be_pandigital(n: int) -> bool:
    """
    Check if n can be pandigital.
    """
    digits = [False] * 10
    if n <= 0:
        return False

    while n > 0:
        digit = n % 10
        if digit == 0:
            return False

        if digits[digit]:
            return False

        digits[digit] = True
        n //= 10

    return True


def solve_with_number_filter() -> int:
    nums = []
    for n in range(10000):
        if can_be_pandigital(n):
            nums.append(n)

    result = set()
    for i, a in enumerate(nums):
        if a > 1000:
            break

        for b in nums[i:]:
            c = a * b
            if check_pandigital(a, b, c):
                result.add(c)

    return sum(result)
