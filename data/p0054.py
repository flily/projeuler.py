#!/usr/bin/env python3
# coding: utf-8


"""
Data of problem 54.
"""


def load():
    with open("data/p0054.txt", encoding="utf-8") as f:
        result = []
        for line in f:
            cards = line.split()
            result.append((cards[:5], cards[5:]))

        return result
