from dataclasses import dataclass, field
from typing import List
from random import shuffle
from entities.card import Card, CardSuit
from entities.hand import Hand


def get_all_cards() -> List[Card]:
    ranks = range(2, 15)
    cards = [Card(suit, rank) for suit in CardSuit for rank in ranks]
    shuffle(cards)

    return cards


@dataclass
class Deck:
    cards: List[Card] = field(default_factory=get_all_cards)

    def shuffle(self) -> List[Card]:
        shuffle(self.cards)

        return self.cards

    def deal(self, hand_count: int = 1) -> List[Hand]:
        if hand_count > 6:
            raise Exception(f"Maximum number of hands is 6")

        cards = self.cards[0:hand_count * 5]

        del self.cards[0:hand_count * 5]

        hands = []

        for i in range(0, len(cards), 5):
            hands.append(Hand(cards[i:i + 5]))

        return hands
