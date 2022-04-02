from dataclasses import dataclass
from typing import TYPE_CHECKING
from rankers.hand_ranker import HandRanker
from rankers.high_card_ranker import HighCardRanker
from utils import get_largest_kind_group

if TYPE_CHECKING:
    from entities.hand import Hand


@dataclass
class KindRanker(HandRanker):
    kind_count: int

    def matches(self, hand: "Hand"):
        cards = get_largest_kind_group(hand.cards)

        return len(cards) == self.kind_count

    def wins_tie(self, hand_a: "Hand", hand_b: "Hand"):
        cards_a = get_largest_kind_group(hand_a.cards)
        cards_b = get_largest_kind_group(hand_b.cards)

        if cards_a[0].rank == cards_b[0].rank:
            return HighCardRanker().wins_tie(hand_a, hand_b)

        if cards_a[0].rank > cards_b[0].rank:
            return True

        return False
