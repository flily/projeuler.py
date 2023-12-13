#!/usr/bin/env python3
# coding: utf-8


"""
Counting Sundays

You are given the following information, but you may prefer to do some research for yourself.

1 Jan 1900 was a Monday.
Thirty days has September,
April, June and November.
All the rest have thirty-one,
Saving February alone,
Which has twenty-eight, rain or shine.
And on leap years, twenty-nine.
A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible
by 400.

How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec
2000)?
"""


PID = 19
ANSWER = 171


MONTH_DAYS = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def is_leap_year(year: int) -> bool:
    """
    Check if the given year is a leap year.
    """
    if year % 4 != 0:
        return False

    if year % 100 == 0:
        return year % 400 == 0

    return True


def solve_by_count() -> int:
    result = 0
    days = 365  # count from 1901-01-01
    for year in range(1901, 2001):
        for month in range(1, 13):
            # 1900-01-01 is Monday, so Sunday is 6 days after
            if days % 7 == 6:
                result += 1

            days += MONTH_DAYS[month]
            if month == 2 and is_leap_year(year):
                days += 1

    return result
