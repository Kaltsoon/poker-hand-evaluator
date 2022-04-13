from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.hand import Hand


class HandRanker:
    def matches(self, hand: "Hand") -> bool:
        raise NotImplementedError()

    def wins_tie(self, hand_a: "Hand", hand_b: "Hand") -> bool:
        raise NotImplementedError()
