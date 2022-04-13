from typing import TYPE_CHECKING
from rankers.hand_ranker import HandRanker

if TYPE_CHECKING:
    from entities.hand import Hand


class HighCardRanker(HandRanker):
    def matches(self, hand: "Hand") -> bool:
        return True

    def wins_tie(self, hand_a: "Hand", hand_b: "Hand") -> bool:
        sorted_cards_a = sorted(hand_a.cards, reverse=True)
        sorted_cards_b = sorted(hand_b.cards, reverse=True)

        for index, card_a in enumerate(sorted_cards_a):
            card_b = sorted_cards_b[index]

            if card_a.rank == card_b.rank:
                continue

            if card_a.rank > card_b.rank:
                return True
            else:
                return False

        return True
