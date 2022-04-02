from typing import TYPE_CHECKING
from rankers.hand_ranker import HandRanker
from rankers.high_card_ranker import HighCardRanker

if TYPE_CHECKING:
    from entities.hand import Hand


class StraightRanker(HandRanker):
    def matches(self, hand: "Hand"):
        straight_hand = hand.to_straight_hand()
        sorted_cards = sorted(straight_hand.cards)

        for index in range(0, len(sorted_cards) - 1):
            card = sorted_cards[index]
            next_card = sorted_cards[index + 1]

            if abs(card.rank - next_card.rank) != 1:
                return False

        return True

    def wins_tie(self, hand_a: "Hand", hand_b: "Hand"):
        return HighCardRanker().wins_tie(
            hand_a.to_straight_hand(),
            hand_b.to_straight_hand()
        )
