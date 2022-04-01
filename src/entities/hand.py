from dataclasses import dataclass
from typing import List, Dict
from enum import IntEnum
from entities.card import Card, CardType


class HandRank(IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9


NAME_BY_RANK = {
    HandRank.HIGH_CARD: "High card",
    HandRank.ONE_PAIR: "One pair",
    HandRank.TWO_PAIR: "Two pair",
    HandRank.THREE_OF_A_KIND: "Three of a kind",
    HandRank.STRAIGHT: "Straight",
    HandRank.FLUSH: "Flush",
    HandRank.FULL_HOUSE: "Full house",
    HandRank.FOUR_OF_A_KIND: "Four of a kind",
    HandRank.STRAIGHT_FLUSH: "Straight flush"
}


@dataclass
class Hand:
    cards: List[Card]

    @property
    def rank(self):
        most_common_rank_cards = self.get_most_common_rank_cards()
        pairs = self.get_pairs()

        if self.is_straight_flush():
            return HandRank.STRAIGHT_FLUSH
        if len(most_common_rank_cards) == 4:
            return HandRank.FOUR_OF_A_KIND
        if self.is_full_house():
            return HandRank.FULL_HOUSE
        if self.is_flush():
            return HandRank.FLUSH
        if self.is_straight():
            return HandRank.STRAIGHT
        if len(most_common_rank_cards) == 3:
            return HandRank.THREE_OF_A_KIND
        if len(pairs) == 2:
            return HandRank.TWO_PAIR
        if len(pairs) == 1:
            return HandRank.ONE_PAIR

        return HandRank.HIGH_CARD

    def is_full_house(self):
        groups = self.group_by_rank()
        card_groups = groups.values()

        three_cards_group = None
        two_card_group = None

        for cards in card_groups:
            if len(cards) == 3:
                three_cards_group = cards
            elif len(cards) == 2:
                two_card_group = cards

        return three_cards_group is not None and two_card_group is not None

    def is_straight(self):
        cards_without_ace = [
            card for card in self.cards if card.type != CardType.ACE]
        sorted_cards = sorted(cards_without_ace)

        for index in range(0, len(sorted_cards) - 1):
            card = sorted_cards[index]
            next_card = sorted_cards[index + 1]

            if abs(card.rank - next_card.rank) != 1:
                return False

        if len(cards_without_ace) == len(self.cards):
            return True

        return sorted_cards[0].rank == 2 or sorted_cards[len(sorted_cards) - 1].type == CardType.KING

    def is_flush(self):
        suit = self.cards[0].suit

        for card in self.cards:
            if card.suit != suit:
                return False

        return True

    def is_straight_flush(self):
        return self.is_flush() and self.is_straight()

    def get_pairs(self):
        groups = self.group_by_rank()
        card_groups = groups.values()
        pairs = [cards for cards in card_groups if len(cards) == 2]

        return pairs

    def get_most_common_rank_cards(self):
        groups = self.group_by_rank()
        card_groups = groups.values()
        sorted_values = sorted(card_groups, key=len, reverse=True)

        return sorted_values[0]

    def group_by_rank(self):
        groups: Dict[int, List[Card]] = {}

        for card in self.cards:
            rank_cards = groups.get(card.rank, [])
            rank_cards.append(card)
            groups[card.rank] = rank_cards

        return groups

    def has_higher_card(self, hand: "Hand"):
        sorted_self_cards = sorted(self.cards, reverse=True)
        sorted_other_cards = sorted(hand.cards, reverse=True)

        for index, card in enumerate(sorted_self_cards):
            if card.rank > sorted_other_cards[index].rank:
                return True

        return False

    def __eq__(self, other: "Hand"):
        if not isinstance(other, Hand) or len(self.cards) != len(other.cards):
            return False

        sorted_self_cards = sorted(self.cards)
        sorted_other_cards = sorted(other.cards)

        for index, card in enumerate(sorted_self_cards):
            other_card = sorted_other_cards[index]

            if (card.rank, card.suit) != (other_card.rank, other_card.suit):
                return False

        return True

    def __gt__(self, other: "Hand"):
        if not isinstance(other, Hand):
            return False

        if self.rank > other.rank:
            return True

        return self.has_higher_card(other)

    def __str__(self):
        hand_string = ", ".join([str(card) for card in self.cards])
        rank_string = NAME_BY_RANK.get(self.rank, "High card")

        return f"{hand_string} ({rank_string})"
