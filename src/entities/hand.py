from dataclasses import dataclass
from typing import List
from enum import IntEnum
from entities.card import Card, CardType
from rankers.pair_ranker import PairRanker
from rankers.kind_ranker import KindRanker
from rankers.straight_ranker import StraightRanker
from rankers.flush_ranker import FlushRanker
from rankers.full_house_ranker import FullHouseRanker
from rankers.combined_ranker import CombinedRanker
from rankers.high_card_ranker import HighCardRanker


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


RANKERS = [
    (
        CombinedRanker([FlushRanker(), StraightRanker()]),
        HandRank.STRAIGHT_FLUSH
    ),
    (KindRanker(4), HandRank.FOUR_OF_A_KIND),
    (FullHouseRanker(), HandRank.FULL_HOUSE),
    (FlushRanker(), HandRank.FLUSH),
    (StraightRanker(), HandRank.STRAIGHT),
    (KindRanker(3), HandRank.THREE_OF_A_KIND),
    (PairRanker(2), HandRank.TWO_PAIR),
    (PairRanker(1), HandRank.ONE_PAIR),
    (HighCardRanker(), HandRank.HIGH_CARD)
]


@dataclass
class Hand:
    cards: List[Card]

    @property
    def rank(self):
        _, rank = self.get_ranker()

        return rank

    def get_ranker(self):
        for ranker, rank in RANKERS:
            if ranker.matches(self):
                return (ranker, rank)

        return (HighCardRanker(), HandRank.HIGH_CARD)

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

        ranker, rank = self.get_ranker()
        other_rank = hand.rank

        if rank > other_rank:
            return True

        if rank == other_rank and ranker.wins_tie(self, hand):
            return True

        return False

    def __str__(self):
        hand_string = ", ".join([str(card) for card in self.cards])
        rank_string = NAME_BY_RANK.get(self.rank, "High card")

        return f"{hand_string} ({rank_string})"
