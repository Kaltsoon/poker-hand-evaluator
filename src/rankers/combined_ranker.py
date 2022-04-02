from dataclasses import dataclass
from typing import TYPE_CHECKING, List
from rankers.hand_ranker import HandRanker

if TYPE_CHECKING:
    from entities.hand import Hand


@dataclass
class CombinedRanker(HandRanker):
    rankers: List[HandRanker]

    def matches(self, hand: "Hand"):
        for ranker in self.rankers:
            if not ranker.matches(hand):
                return False

        return True

    def wins_tie(self, hand_a: "Hand", hand_b: "Hand"):
        for ranker in self.rankers:
            if ranker.wins_tie(hand_a, hand_b):
                return True
        
        return False
