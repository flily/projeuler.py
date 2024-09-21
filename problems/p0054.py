#!/usr/bin/env python3
# coding: utf-8


"""
Poker Hands

In the card game poker, a hand consists of five cards and are ranked, from lowest to highest, in
the following way:
        - High Card: Highest value card.
        - One Pair: Two cards of the same value.
        - Two Pairs: Two different pairs.
        - Three of a Kind: Three cards of the same value.
        - Straight: All cards are consecutive values.
        - Flush: All cards of the same suit.
        - Full House: Three of a kind and a pair.
        - Four of a Kind: Four cards of the same value.
        - Straight Flush: All cards are consecutive values of same suit.
        - Royal Flush: Ten, Jack, Queen, King, Ace, in same suit.

The cards are valued in the order:
    2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace.

If two players have the same ranked hands then the rank made up of the highest value wins; for
example, a pair of eights beats a pair of fives (see example 1 below). But if two ranks tie, for
example, both players have a pair of queens, then highest cards in each hand are compared (see
example 4 below); if the highest cards tie then the next highest cards are compared, and so on.

Consider the following five hands dealt to two players:
Hand    Player 1            Player 2            Winner
1       5H 5C 6S 7S KD      2C 3S 8S 8D TD      Player 2
        Pair of Fives       Pair of Eights

2       5D 8C 9S JS AC      2C 5C 7D 8S QH      Player 1
        Highest card Ace    Highest card Queen

3       2D 9C AS AH AC      3D 6D 7D TD QD      Player 2
        Three Aces          Flush with Diamonds

4       4D 6S 9H QH QC      3D 6D 7H QD QS      Player 1
        Pair of Queens      Pair of Queens
        Highest card Nine   Highest card Seven

5       2H 2D 4C 4D 4S      3C 3D 3S 9S 9D      Player 1
        Full House          Full House
        With Three Fours    with Three Threes

The file, poker.txt, contains one-thousand random hands dealt to two players. Each line of the file
contains ten cards (separated by a single space): the first five are Player 1's cards and the last
five are Player 2's cards. You can assume that all hands are valid (no invalid characters or
repeated cards), each player's hand is in no specific order, and in each hand there is a clear
winner.

How many hands does Player 1 win?
"""


from __future__ import annotations

from typing import Iterable

from data import load


ANSWER = 376


CARD_VALUE_MAP = {
    "2": (2, " 2"),
    "3": (3, " 3"),
    "4": (4, " 4"),
    "5": (5, " 5"),
    "6": (6, " 6"),
    "7": (7, " 7"),
    "8": (8, " 8"),
    "9": (9, " 9"),
    "T": (10, "10"),
    "J": (11, " J"),
    "Q": (12, " Q"),
    "K": (13, " K"),
    "A": (14, " A"),
}


KIND_SPADE = "♠"
KIND_HEART = "♥"
KIND_CLUB = "♣"
KIND_DIAMOND = "♦"
KIND_MAP = {
    "S": "♠",
    "H": "♥",
    "C": "♣",
    "D": "♦",
}


class Card:
    """
    A playing card.
    """

    Jack = 11
    Queen = 12
    King = 13
    Ace = 14

    def __init__(self, card: str) -> None:
        value, display = CARD_VALUE_MAP[card[0]]
        self.value = value
        self.display = display
        self.kind = KIND_MAP[card[1]]

    def __gt__(self, other: Card) -> bool:
        return self.value > other.value

    def __repr__(self) -> str:
        return f"{self.display}{self.kind}"


class Hands:
    """
    A poker hand.
    """

    HighCard = 1
    OnePair = 2
    TwoPairs = 3
    ThreeOfAKind = 4
    Straight = 5
    Flush = 6
    FullHouse = 7
    FourOfAKind = 8
    StraightFlush = 9
    RoyalFlush = 10

    def __init__(self, cards: Iterable[Card]) -> None:
        self.cards = list(cards)
        self.cards.sort(key=lambda card: card.value)

    def __repr__(self) -> str:
        content = " ".join([str(card) for card in self.cards])
        return f"[{content}]"

    def _is_flush(self) -> tuple[str | None, Card]:
        kind = self.cards[0].kind
        for card in self.cards:
            if card.kind != kind:
                return None, None

        return kind, self.cards[-1]

    def _is_straight(self) -> tuple[bool, Card]:
        for i in range(1, len(self.cards)):
            if self.cards[i].value - 1 != self.cards[i - 1].value:
                return False, None

        return True, self.cards[-1]

    def _is_flush_or_straight(self) -> tuple[bool, Iterable[tuple[int, Card]]]:
        is_flush, flush_value = self._is_flush()
        is_straight, straight_value = self._is_straight()
        if is_flush is not None and is_straight:
            if straight_value.value == Card.Ace:
                return True, [(Hands.RoyalFlush, flush_value)]

            return True, [(Hands.StraightFlush, straight_value)]

        if is_straight:
            return True, [(Hands.Straight, straight_value)]

        if is_flush:
            return True, [(Hands.Flush, x) for x in self.cards]

        return False, []

    def get_rank(self) -> Iterable[tuple[int, Card]]:
        """
        Check the rank of the hand.
        """
        is_flush_or_straight, result = self._is_flush_or_straight()
        if is_flush_or_straight:
            return result

        result = []
        value_map = {}
        for card in self.cards:
            cards = value_map.get(card.value, [])
            cards.append(card)
            value_map[card.value] = cards

        pairs = 0
        for _, cards in value_map.items():
            if len(cards) == 4:
                item = (self.FourOfAKind, cards[0])

            elif len(cards) == 3:
                item = (self.ThreeOfAKind, cards[0])

            elif len(cards) == 2:
                pairs += 1
                item = (self.OnePair, cards[0])

            else:
                item = (self.HighCard, cards[0])

            result.append(item)

        result.sort(key=lambda item: (item[0], item[1]), reverse=True)
        if len(result) == 2:
            # fix full house
            if result[0][0] == Hands.ThreeOfAKind and result[1][0] == Hands.OnePair:
                result = [(Hands.FullHouse, result[0][1])]

        elif pairs == 2:
            # fix two pairs
            result[0] = (Hands.TwoPairs, result[0][1])
            result[1] = (Hands.TwoPairs, result[1][1])

        return result

    @staticmethod
    def hand_name(name: int) -> str:
        """
        Get the name of the hand.
        """
        m = {
            Hands.HighCard: "High Card",
            Hands.OnePair: "One Pair",
            Hands.TwoPairs: "Two Pairs",
            Hands.ThreeOfAKind: "Three of a Kind",
            Hands.Straight: "Straight",
            Hands.Flush: "Flush",
            Hands.FullHouse: "Full House",
            Hands.FourOfAKind: "Four of a Kind",
            Hands.StraightFlush: "Straight Flush",
            Hands.RoyalFlush: "Royal Flush",
        }
        return m[name]


def check_hands(hand_a: Hands, hand_b: Hands) -> int:
    """
    Check the hands if player a wins.
    """
    rank_a = hand_a.get_rank()
    rank_b = hand_b.get_rank()
    # print(f"A {hand_a} vs B {hand_b}")
    # print(f"    A {rank_a}")
    # print(f"    B {rank_b}")

    i = 0
    finished = False
    result = False
    while not finished and i < len(rank_a) and i < len(rank_b):
        if rank_a[i] > rank_b[i]:
            rs = "Player 1 Win"
            result = True
            finished = True

        elif rank_a[i] < rank_b[i]:
            rs = "Player 2 Win"
            finished = True

        else:
            rs = "Tie"

        # print(f"    - A {Hands.hand_name(rank_a[i][0])} {rank_a[i][1]}")
        # print(f"    - B {Hands.hand_name(rank_b[i][0])} {rank_b[i][1]}")
        # print(f"    - {rs}")
        # print("    ------")
        del rs
        i += 1

    return result


def solve() -> int:
    result = 0
    for player_a, player_b in load():
        hand_a = Hands([Card(card) for card in player_a])
        hand_b = Hands([Card(card) for card in player_b])

        if check_hands(hand_a, hand_b):
            result += 1

    return result
