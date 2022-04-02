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
        largest_kind_group = self.get_largest_kind_group()
        pairs = self.get_pairs()

        if self.is_straight_flush():
            return HandRank.STRAIGHT_FLUSH
        if len(largest_kind_group) == 4:
            return HandRank.FOUR_OF_A_KIND
        if self.is_full_house():
            return HandRank.FULL_HOUSE
        if self.is_flush():
            return HandRank.FLUSH
        if self.is_straight():
            return HandRank.STRAIGHT
        if len(largest_kind_group) == 3:
            return HandRank.THREE_OF_A_KIND
        if len(pairs) == 2:
            return HandRank.TWO_PAIR
        if len(pairs) == 1:
            return HandRank.ONE_PAIR

        return HandRank.HIGH_CARD

    def to_straight_hand(self):
        cards_without_aces = [
            card for card in self.cards if card.type != CardType.ACE
        ]

        min_card = min(cards_without_aces)
        ace_rank = 1 if min_card.rank == 2 else 14

        normalized_cards = [
            Card(
                card.suit,
                card.rank if card.type != CardType.ACE else ace_rank
            )
            for card in self.cards
        ]

        return Hand(normalized_cards)

    def is_full_house(self):
        three_of_a_kind_group, two_of_a_kind_group = self.get_full_house_groups()

        return three_of_a_kind_group is not None and two_of_a_kind_group is not None

    def is_straight(self):
        hand = self.to_straight_hand()
        sorted_cards = sorted(hand.cards)

        for index in range(0, len(sorted_cards) - 1):
            card = sorted_cards[index]
            next_card = sorted_cards[index + 1]

            if abs(card.rank - next_card.rank) != 1:
                return False

        return True

    def is_flush(self):
        suit = self.cards[0].suit

        for card in self.cards:
            if card.suit != suit:
                return False

        return True

    def is_straight_flush(self):
        return self.is_flush() and self.is_straight()

    def get_largest_kind_group(self):
        groups = self.group_cards_by_rank()
        card_groups = groups.values()
        sorted_values = sorted(card_groups, key=len, reverse=True)

        return sorted_values[0]

    def group_cards_by_rank(self):
        groups: Dict[int, List[Card]] = {}

        for card in self.cards:
            rank_cards = groups.get(card.rank, [])
            rank_cards.append(card)
            groups[card.rank] = rank_cards

        return groups

    def get_pairs(self):
        groups = self.group_cards_by_rank()
        card_groups = groups.values()
        pairs = [cards for cards in card_groups if len(cards) == 2]

        sorted_pairs = sorted(
            pairs, key=lambda pair: pair[0].rank, reverse=True
        )

        return sorted_pairs

    def get_largest_kind_group(self):
        groups = self.group_cards_by_rank()
        card_groups = groups.values()
        sorted_values = sorted(card_groups, key=len, reverse=True)

        return sorted_values[0]

    def get_full_house_groups(self):
        groups = self.group_cards_by_rank()
        card_groups = groups.values()

        three_of_a_kind_group = None
        two_of_a_kind_group = None

        for cards in card_groups:
            if len(cards) == 3:
                three_of_a_kind_group = cards
            elif len(cards) == 2:
                two_of_a_kind_group = cards

        return (two_of_a_kind_group, three_of_a_kind_group)

    def wins_tie(self, hand: "Hand"):
        rank = self.rank

        if rank == HandRank.HIGH_CARD:
            return self.wins_high_card_tie(hand)
        if rank == HandRank.ONE_PAIR or rank == HandRank.TWO_PAIR:
            return self.wins_pair_tie(hand)
        if rank == HandRank.THREE_OF_A_KIND or rank == HandRank.FOUR_OF_A_KIND:
            return self.wins_n_of_a_kind_tie(hand)
        if rank == HandRank.FLUSH:
            return self.wins_high_card_tie(hand)
        if rank == HandRank.FULL_HOUSE:
            return self.wins_full_house_tie(hand)
        if rank == HandRank.STRAIGHT or rank == HandRank.STRAIGHT_FLUSH:
            return self.wins_straight_tie(hand)

        return True

    def wins_high_card_tie(self, hand: "Hand"):
        sorted_cards_a = sorted(self.cards, reverse=True)
        sorted_cards_b = sorted(hand.cards, reverse=True)

        for index, card_a in enumerate(sorted_cards_a):
            card_b = sorted_cards_b[index]

            if card_a.rank == card_b.rank:
                continue

            if card_a.rank > card_b.rank:
                return True
            else:
                return False

        return True

    def wins_pair_tie(self, hand: "Hand"):
        pairs_a = self.get_pairs()
        pairs_b = hand.get_pairs()

        for index, pair_a in enumerate(pairs_a):
            pair_b = pairs_b[index]

            if pair_a[0].rank == pair_b[0].rank:
                continue

            if pair_a[0].rank > pair_b[0].rank:
                return True
            else:
                return False

        return self.wins_high_card_tie(hand)

    def wins_n_of_a_kind_tie(self, hand: "Hand"):
        cards_a = self.get_largest_kind_group()
        cards_b = hand.get_largest_kind_group()

        if cards_a[0].rank == cards_b[0].rank:
            return self.wins_high_card_tie(hand)

        if cards_a[0].rank > cards_b[0].rank:
            return True

        return False

    def wins_full_house_tie(self, hand: "Hand"):
        two_of_a_kind_group_a, three_of_a_kind_group_a = self.get_full_house_groups()
        two_of_a_kind_group_b, three_of_a_kind_group_b = hand.get_full_house_groups()

        if three_of_a_kind_group_a[0].rank > three_of_a_kind_group_b[0].rank:
            return True
        if three_of_a_kind_group_b[0].rank > three_of_a_kind_group_a[0].rank:
            return False
        if two_of_a_kind_group_a[0].rank > two_of_a_kind_group_b[0].rank:
            return True

        return False

    def wins_straight_tie(self, hand: "Hand"):
        return self.to_straight_hand().wins_high_card_tie(hand.to_straight_hand())

    def __eq__(self, hand: "Hand"):
        if not isinstance(hand, Hand) or len(self.cards) != len(hand.cards):
            return False

        sorted_self_cards = sorted(self.cards)
        sorted_other_cards = sorted(hand.cards)

        for index, card in enumerate(sorted_self_cards):
            other_card = sorted_other_cards[index]

            if (card.rank, card.suit) != (other_card.rank, other_card.suit):
                return False

        return True

    def __gt__(self, hand: "Hand"):
        if not isinstance(hand, Hand):
            return False

        if self.rank > hand.rank:
            return True

        if self.rank == hand.rank and self.wins_tie(hand):
            return True

        return False

    def __str__(self):
        hand_string = ", ".join([str(card) for card in self.cards])
        rank_string = NAME_BY_RANK.get(self.rank, "High card")

        return f"{hand_string} ({rank_string})"
