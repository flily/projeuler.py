#!/usr/bin/env python3
# coding: utf-8


"""
Coded Triangle Numbers

The nth term of the sequence of triangle numbers is given by, t(n) = (1/2)*n(n+1); so the first ten
triangle numbers are:
        1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

By converting each letter in a word to a number corresponding to its alphabetical position and
adding these values we form a word value. For example, the word value for SKY is
19 + 11 + 25 = 55 = t(10). If the word value is a triangle number then we shall call the word a
triangle word.

Using words.txt (right click and 'Save Link/Target As...'), a 16K text file containing nearly
two-thousand common English words, how many are triangle words?
"""


from data import load


ANSWER = 162


def triangle_number(n: int) -> int:
    """
    Get the nth triangle number.
    """
    return n * (n + 1) // 2


def word_score(word: str) -> int:
    """
    Get the word score.
    """
    result = 0
    for c in word.upper():
        result += ord(c) - 64  # ord('A') == 65

    return result


def solve_naive() -> int:
    triangle_numbers = set()
    for i in range(1, 20):
        triangle_numbers.add(triangle_number(i))

    result = 0
    for word in load():
        score = word_score(word)
        if score in triangle_numbers:
            result += 1

    return result
