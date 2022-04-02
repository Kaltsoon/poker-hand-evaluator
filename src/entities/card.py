from dataclasses import dataclass, field
from enum import Enum, IntEnum, auto


class CardSuit(Enum):
    CLUB = auto()
    DIAMOND = auto()
    HEART = auto()
    SPADE = auto()


class CardType(IntEnum):
    NUMERAL = 0
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


SYMBOL_BY_SUIT = {
    CardSuit.CLUB: "♣",
    CardSuit.DIAMOND: "♦",
    CardSuit.HEART: "♥",
    CardSuit.SPADE: "♠"
}

NAME_BY_TYPE = {
    CardType.JACK: "J",
    CardType.QUEEN: "Q",
    CardType.KING: "K",
    CardType.ACE: "A"
}


@dataclass(order=True)
class Card:
    suit: CardSuit = field(compare=False)
    rank: int

    @property
    def type(self):
        if self.rank == 1:
            return CardType.ACE

        if self.rank <= 10:
            return CardType.NUMERAL

        return CardType(self.rank)

    def __str__(self):
        name = NAME_BY_TYPE.get(self.type, self.rank)
        symbol = SYMBOL_BY_SUIT[self.suit]

        return f"{name} {symbol}"
