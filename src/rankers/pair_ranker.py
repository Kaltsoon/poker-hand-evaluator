from dataclasses import dataclass
from typing import TYPE_CHECKING
from rankers.hand_ranker import HandRanker
from rankers.high_card_ranker import HighCardRanker
from utils import get_pairs

if TYPE_CHECKING:
    from entities.hand import Hand


@dataclass
class PairRanker(HandRanker):
    pair_count: int

    def matches(self, hand: "Hand") -> bool:
        pairs = get_pairs(hand.cards)

        return len(pairs) == self.pair_count

    def wins_tie(self, hand_a: "Hand", hand_b: "Hand") -> bool:
        pairs_a = get_pairs(hand_a.cards)
        pairs_b = get_pairs(hand_b.cards)

        for index, pair_a in enumerate(pairs_a):
            pair_b = pairs_b[index]

            if pair_a[0].rank == pair_b[0].rank:
                continue

            if pair_a[0].rank > pair_b[0].rank:
                return True
            else:
                return False

        return HighCardRanker().wins_tie(hand_a, hand_b)
