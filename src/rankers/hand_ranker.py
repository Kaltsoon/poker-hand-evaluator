from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.hand import Hand


class HandRanker:
    def matches(self, hand: "Hand"):
        raise NotImplementedError()

    def wins_tie(self, hand_a: "Hand", hand_b: "Hand"):
        raise NotImplementedError()
