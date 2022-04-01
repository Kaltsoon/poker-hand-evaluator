from entities.deck import Deck

deck = Deck()

def main():
    deck = Deck()

    hands = deck.deal()

    print(hands[0])

if __name__ == "__main__":
    main()
