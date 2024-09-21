#!/usr/bin/env python3
# coding: utf-8


"""
XOR Decryption

Each character on a computer is assigned a unique code and the preferred standard is ASCII
(American Standard Code for Information Interchange). For example, uppercase A = 65,
asterisk (*) = 42, and lowercase k = 107.

A modern encryption method is to take a text file, convert the bytes to ASCII, then XOR each byte
with a given value, taken from a secret key. The advantage with the XOR function is that using the
same encryption key on the cipher text, restores the plain text; for example, 65 XOR 42 = 107,
then 107 XOR 42 = 65.

For unbreakable encryption, the key is the same length as the plain text message, and the key is
made up of random bytes. The user would keep the encrypted message and the encryption key in
different locations, and without both "halves", it is impossible to decrypt the message.

Unfortunately, this method is impractical for most users, so the modified method is to use a
password as a key. If the password is shorter than the message, which is likely, the key is
repeated cyclically throughout the message. The balance for this method is using a sufficiently
long password key for security, but short enough to be memorable.

Your task has been made easy, as the encryption key consists of three lower case characters. Using
p059_cipher.txt, a file containing the encrypted ASCII codes, and the knowledge that the plain text
must contain common English words, decrypt the message and find the sum of the ASCII values in the
original text.
"""


import itertools
from typing import Iterable

from data import load


ANSWER = 129448


def decrypt(cipher: Iterable[int], key: Iterable[int]) -> Iterable[int]:
    """
    Decrypt cipher with key.
    """
    plain = [0] * len(cipher)
    for i, c in enumerate(cipher):
        plain[i] = c ^ key[i % len(key)]

    return plain


def readable_filter(plain: Iterable[int]) -> bool:
    """
    Check if plain is readable.
    """
    for p in plain:
        if p < 32 or p > 126:
            return False

    return True


def solve_naive() -> int:
    char_a = ord("a")
    char_z = ord("z")
    cipher = load()
    for key in itertools.product(range(char_a, char_z + 1), repeat=3):
        plain = decrypt(cipher, key)
        if not readable_filter(plain):
            continue

        plain_str = "".join(chr(p) for p in plain)
        if "the " not in plain_str:
            continue

        return sum(plain)

    return 0


def readable_filter_with_state_machine(plain: Iterable[int]) -> bool:
    """
    Check if plain is readable. Find 'the ' in plain.

    State 0: INIT
    State 1: t
    State 2: th
    State 3: the
    State 4: the_

    ASCII: 116 104 101  32
             t   h   e ' '
    """
    state = 0
    for p in plain:
        if p < 32 or p > 126:
            return False

        if state == 0 and p == 116:
            state = 1

        elif state == 1 and p == 104:
            state = 2

        elif state == 2 and p == 101:
            state = 3

        elif state == 3 and p == 32:
            return True

        else:
            state = 0

    return False


def solve_with_state_machine() -> int:
    char_a = ord("a")
    char_z = ord("z")
    cipher = load()
    for key in itertools.product(range(char_a, char_z + 1), repeat=3):
        plain = decrypt(cipher, key)
        if not readable_filter_with_state_machine(plain):
            continue

        return sum(plain)

    return 0


def readable_filter_with_buffer(plain: Iterable[int]) -> bool:
    """
    Check if plain is readable. Find 'the ' in plain.

    ASCII:  0x74  0x68  0x65  0x20
              t     h     e    ' '
    """
    flag = 0x74686520
    cache = 0
    for p in plain:
        if p < 32 or p > 126:
            return False

        cache = ((cache << 8) | p) & 0xffffffff
        if cache == flag:
            return True

    return False


def solve_with_buffer() -> int:
    char_a = ord("a")
    char_z = ord("z")
    cipher = load()
    for key in itertools.product(range(char_a, char_z + 1), repeat=3):
        plain = decrypt(cipher, key)
        if not readable_filter_with_buffer(plain):
            continue

        return sum(plain)

    return 0
