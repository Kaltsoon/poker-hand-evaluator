from entities.deck import Deck

deck = Deck()


def main():
    deck = Deck()

    hand1, hand2 = deck.deal(2)

    print(f"Hand 1: {hand1}")
    print(f"Hand 2: {hand2}")

    winning_hand = "Hand 1" if hand1 > hand2 else "Hand 2"

    print(f"{winning_hand} wins")


if __name__ == "__main__":
    main()
