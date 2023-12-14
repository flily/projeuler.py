#!/usr/bin/env python3
# coding: utf-8


"""
Names Scores

Using names.txt (right click and 'Save Link/Target As...'), a 46K text file containing over
five-thousand first names, begin by sorting it into alphabetical order. Then working out the
alphabetical value for each name, multiply this value by its alphabetical position in the list to
obtain a name score.

For example, when the list is sorted into alphabetical order, COLIN, which is worth
3 + 15 + 12 + 9 + 14 = 53, is the 938th name in the list. So, COLIN would obtain a score of
938 × 53 = 49714.

What is the total of all the name scores in the file?
"""

from data import load


PID = 22
ANSWER = 871198282


def name_score(name: str) -> int:
    """
    Get the name score of name.
    """
    result = 0
    for c in name:
        result += ord(c) - 64  # ord('A') == 65

    return result


def solve() -> int:
    result = 0
    name_list = load()
    name_list.sort()
    for i, name in enumerate(name_list):
        score = name_score(name) * (i + 1)
        result += score

    return result
