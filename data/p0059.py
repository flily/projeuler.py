#!/usr/bin/env python3
# coding: utf-8

"""
Data of problem 59.
"""


def load():
    with open("data/p0059.txt", encoding="utf-8") as f:
        all_data = f.read()
        bytes_str = all_data.split(",")
        return [int(b) for b in bytes_str]
