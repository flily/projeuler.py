#!/usr/bin/env python3
# coding: utf-8


"""
Number Letter Counts

If the numbers 1 to 5 are written out in words: one, two, three, four, five, then there are 
3 + 3 + 5 + 4 + 4 = 19 letters used in total.

If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, how many
letters would be used?


NOTE: Do not count spaces or hyphens. For example, 342 (three hundred and forty-two) contains
23 letters and 115 (one hundred and fifteen) contains 20 letters. The use of "and" when writing out
numbers is in compliance with British usage.
"""


PID = 17
ANSWER = 21124


NUMBERS = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
    20: "twenty",
    30: "thirty",
    40: "forty",
    50: "fifty",
    60: "sixty",
    70: "seventy",
    80: "eighty",
    90: "ninety",
    100: "hundred",
    1000: "thousand",
}


def number_in_english_1000(n: int) -> str:
    """
    Get the English representation of n, where n is in [1, 1000].
    """
    if n == 1000:
        return "one thousand"

    r = []
    if n >= 100:
        hundreds = n // 100
        n = n % 100
        r.append(f"{NUMBERS[hundreds]} hundred")

    if n == 0:
        return " ".join(r)

    if len(r) > 0:
        r.append("and")

    if n >= 20:
        tens = n // 10 * 10
        n = n % 10

        if n == 0:
            r.append(NUMBERS[tens])
        else:
            r.append(f"{NUMBERS[tens]}-{NUMBERS[n]}")

    elif n > 0:
        r.append(NUMBERS[n])

    return " ".join(r)


def letter_count(n: str) -> int:
    """
    Get the number of letters in n.
    """
    return len(n.replace(" ", "").replace("-", ""))


def solve() -> int:
    s = 0
    i = 1
    while i <= 1000:
        english_number = number_in_english_1000(i)
        c = letter_count(english_number)
        s += c
        i += 1

    return s
