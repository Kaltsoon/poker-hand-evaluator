from typing import TYPE_CHECKING
from rankers.hand_ranker import HandRanker
from rankers.high_card_ranker import HighCardRanker

if TYPE_CHECKING:
    from entities.hand import Hand


class FlushRanker(HandRanker):
    def matches(self, hand: "Hand"):
        suit = hand.cards[0].suit

        for card in hand.cards:
            if card.suit != suit:
                return False

        return True

    def wins_tie(self, hand_a: "Hand", hand_b: "Hand"):
        return HighCardRanker().wins_tie(hand_a, hand_b)
