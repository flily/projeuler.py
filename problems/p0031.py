#!/usr/bin/env python3
# coding: utf-8


"""
Coin Sums

In the United Kingdom the currency is made up of pound (£) and pence (p). There are eight coins in
general circulation:

    1p, 2p, 5p, 10p, 20p, 50p, £1 (100p), and £2 (200p).

It is possible to make £2 in the following way:

    1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p
How many different ways can £2 be made using any number of coins?
"""


from typing import (
    Iterable,
)
import math
import itertools


ANSWER = 73682


COIN_TYPES = [200, 100, 50, 20, 10, 5, 2, 1]


def make_coins(pences: int, coins: Iterable[int]) -> Iterable[int]:
    """
    Make coins from pences
    """
    result = [0] * len(coins)
    i = 0
    while i < len(coins) and pences > 0:
        result[i] = pences // coins[i]
        pences %= coins[i]
        i -= 1

    return result


def coins_sum(coins: Iterable[int], coins_type: Iterable[int]) -> int:
    """
    Sum of coins
    """
    result = 0
    for i in range(min(len(coins), len(coins_type))):
        result += coins[i] * coins_type[i]

    return result


def count_brute_force(pences: int, coins: Iterable[int]) -> int:
    """
    Brute force solution
    """
    coin_max = [0] * len(coins)
    for i, value in enumerate(coins):
        coin_max[i] = range(math.ceil(pences / value) + 1)

    result = 0
    for coin_count in itertools.product(*coin_max):
        s = coins_sum(coin_count, coins)
        if s == pences:
            result += 1

    return result


def solve_by_brute_force() -> int:
    result = count_brute_force(200, COIN_TYPES)
    return result


def count_brute_force_and_check(pences: int, coins: Iterable[int]) -> int:
    """
    Brute force with check
    """
    coin_max = [0] * len(coins)
    for i, value in enumerate(coins):
        coin_max[i] = math.ceil(pences / value)

    result = 0
    count = [0] * len(coins)
    s = 0
    finished = False
    while not finished:
        if pences - s <= coins[-1] * coin_max[-1]:
            count[-1] = pences - s
            result += 1

        finished = True
        for x in range(len(count) - 2, -1, -1):
            count[x] += 1
            s += coins[x]
            if s > pences:
                s -= count[x] * coins[x]
                count[x] = 0
                continue

            if count[x] > coin_max[x]:
                s -= count[x] * coins[x]
                count[x] = 0
            else:
                finished = False
                break

    return result


def solve_by_brute_force_check() -> int:
    result = count_brute_force_and_check(200, COIN_TYPES)
    return result
