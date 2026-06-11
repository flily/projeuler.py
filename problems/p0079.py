#!/usr/bin/env python3
# coding: utf-8


"""
Passcode Derivation

A common security method used for online banking is to ask the user for three random characters
from a passcode. For example, if the passcode was 531278, they may ask for the 2nd, 3rd, and
5th characters; the expected reply would be: 317.

The text file, keylog.txt, contains fifty successful login attempts.

Given that the three characters are always asked for in order, analyse the file so as to determine
the shortest possible secret passcode of unknown length.
"""

from data import load


ANSWER = 73162890


def data_handler(raw: str) -> list[list[int]]:
    result = []

    for line in raw.splitlines():
        attempt = int(line)
        result.append(attempt)

    return result


def check_success(passcode:int, attempt: int) -> bool:
    p, a = passcode, attempt
    while p > 0 and a > 0:
        if p % 10 == a % 10:
            a //= 10

        p //= 10

    return a == 0


def solve_naive() -> int:
    attempts = load(data_handler)
    for passcode in range(100_000, 100_000_000):
        success = True
        for attempt in attempts:
            if not check_success(passcode, attempt):
                success = False
                break

        if success:
            return passcode

    return 0


def get_digits(n: int) -> list[int]:
    digits = []
    while n > 0:
        digits.append(n % 10)
        n //= 10

    return digits

def update_relation(relations: list[list[list[int], list[int]]], a: int, b: int):
    # b after a
    _, a_next = relations[a]
    if b not in a_next:
        a_next.append(b)

    b_prev, _ = relations[b]
    if a not in b_prev:
        b_prev.append(a)

def solve_sort() -> int:
    attempts = load(data_handler)
    relations = []
    for _ in range(10):
        # previous and next digits
        relations.append([[], []])

    for attempt in attempts:
        digits = get_digits(attempt)
        for i in range(len(digits) - 1):
            for j in range(i + 1, len(digits)):
                a, b = digits[i], digits[j]
                update_relation(relations, a, b)

    digits = []
    for n, (n_prev, n_next) in enumerate(relations):
        if not n_prev and not n_next:
            continue

        digits.append((n, len(n_next)))

    digits.sort(key=lambda x: x[1])

    result = 0
    for digit, _ in digits:
        result = result * 10 + digit

    return result
