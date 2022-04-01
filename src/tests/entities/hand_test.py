import unittest
from entities.hand import Hand, HandRank
from entities.card import Card, CardSuit


class TestHand(unittest.TestCase):
    def test_straight_flush(self):
        hand = Hand([
            Card(CardSuit.DIAMOND, 2),
            Card(CardSuit.DIAMOND, 3),
            Card(CardSuit.DIAMOND, 4),
            Card(CardSuit.DIAMOND, 5),
            Card(CardSuit.DIAMOND, 6)
        ])

        self.assertEqual(hand.rank, HandRank.STRAIGHT_FLUSH)

    def test_four_of_a_kind(self):
        hand = Hand([
            Card(CardSuit.DIAMOND, 2),
            Card(CardSuit.HEART, 3),
            Card(CardSuit.SPADE, 2),
            Card(CardSuit.DIAMOND, 2),
            Card(CardSuit.CLUB, 2)
        ])

        self.assertEqual(hand.rank, HandRank.FOUR_OF_A_KIND)

    def test_full_house(self):
        hand = Hand([
            Card(CardSuit.DIAMOND, 2),
            Card(CardSuit.HEART, 3),
            Card(CardSuit.SPADE, 2),
            Card(CardSuit.DIAMOND, 2),
            Card(CardSuit.CLUB, 3)
        ])

        self.assertEqual(hand.rank, HandRank.FULL_HOUSE)

    def _test_flush(self):
        hand = Hand([
            Card(CardSuit.HEART, 2),
            Card(CardSuit.HEART, 3),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.HEART, 2),
            Card(CardSuit.HEART, 6)
        ])

        self.assertEqual(hand.rank, HandRank.FLUSH)

    def test_straight(self):
        hand_without_ace = Hand([
            Card(CardSuit.DIAMOND, 2),
            Card(CardSuit.CLUB, 5),
            Card(CardSuit.DIAMOND, 4),
            Card(CardSuit.HEART, 3),
            Card(CardSuit.SPADE, 6)
        ])

        hand_with_low_ace = Hand([
            Card(CardSuit.DIAMOND, 14),
            Card(CardSuit.CLUB, 3),
            Card(CardSuit.DIAMOND, 4),
            Card(CardSuit.DIAMOND, 2),
            Card(CardSuit.HEART, 5)
        ])

        hand_with_high_ace = Hand([
            Card(CardSuit.DIAMOND, 14),
            Card(CardSuit.CLUB, 13),
            Card(CardSuit.DIAMOND, 11),
            Card(CardSuit.DIAMOND, 10),
            Card(CardSuit.HEART, 12)
        ])

        self.assertEqual(hand_without_ace.rank, HandRank.STRAIGHT)
        self.assertEqual(hand_with_low_ace.rank, HandRank.STRAIGHT)
        self.assertEqual(hand_with_high_ace.rank, HandRank.STRAIGHT)

    def test_three_of_a_kind(self):
        hand = Hand([
            Card(CardSuit.HEART, 2),
            Card(CardSuit.SPADE, 3),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.DIAMOND, 3),
            Card(CardSuit.HEART, 3)
        ])

        self.assertEqual(hand.rank, HandRank.THREE_OF_A_KIND)

    def test_two_pair(self):
        hand = Hand([
            Card(CardSuit.HEART, 2),
            Card(CardSuit.SPADE, 3),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.DIAMOND, 3),
            Card(CardSuit.HEART, 2)
        ])

        self.assertEqual(hand.rank, HandRank.TWO_PAIR)

    def test_one_pair(self):
        hand = Hand([
            Card(CardSuit.HEART, 2),
            Card(CardSuit.SPADE, 3),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.DIAMOND, 5),
            Card(CardSuit.HEART, 2)
        ])

        self.assertEqual(hand.rank, HandRank.ONE_PAIR)

    def test_high_card(self):
        hand = Hand([
            Card(CardSuit.HEART, 2),
            Card(CardSuit.SPADE, 3),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.DIAMOND, 5),
            Card(CardSuit.HEART, 10)
        ])

        self.assertEqual(hand.rank, HandRank.HIGH_CARD)

    def test_equality(self):
        hand_a = Hand([
            Card(CardSuit.HEART, 10),
            Card(CardSuit.SPADE, 3),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.DIAMOND, 5),
            Card(CardSuit.HEART, 2)
        ])

        hand_b = Hand([
            Card(CardSuit.HEART, 2),
            Card(CardSuit.SPADE, 3),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.DIAMOND, 5),
            Card(CardSuit.HEART, 10)
        ])

        self.assertTrue(hand_a == hand_b)

    def test_comparisons(self):
        hand_one_pair = Hand([
            Card(CardSuit.HEART, 2),
            Card(CardSuit.SPADE, 3),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.DIAMOND, 5),
            Card(CardSuit.HEART, 2)
        ])

        hand_high_card = Hand([
            Card(CardSuit.HEART, 2),
            Card(CardSuit.SPADE, 3),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.DIAMOND, 5),
            Card(CardSuit.HEART, 10)
        ])

        self.assertTrue(hand_one_pair > hand_high_card)
        self.assertTrue(hand_high_card < hand_one_pair)

    def test_high_card_tie(self):
        hand_a = Hand([
            Card(CardSuit.HEART, 2),
            Card(CardSuit.SPADE, 3),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.DIAMOND, 5),
            Card(CardSuit.HEART, 11)
        ])

        hand_b = Hand([
            Card(CardSuit.HEART, 2),
            Card(CardSuit.SPADE, 3),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.DIAMOND, 5),
            Card(CardSuit.HEART, 10)
        ])

        self.assertTrue(hand_a > hand_b)

    def test_one_pair_tie(self):
        hand_a = Hand([
            Card(CardSuit.HEART, 4),
            Card(CardSuit.SPADE, 3),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.DIAMOND, 5),
            Card(CardSuit.HEART, 11)
        ])

        hand_b = Hand([
            Card(CardSuit.HEART, 2),
            Card(CardSuit.SPADE, 3),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.DIAMOND, 5),
            Card(CardSuit.HEART, 3)
        ])

        self.assertTrue(hand_a > hand_b)
    
    def test_two_pair_tie(self):
        hand_a = Hand([
            Card(CardSuit.HEART, 4),
            Card(CardSuit.SPADE, 5),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.DIAMOND, 5),
            Card(CardSuit.HEART, 11)
        ])

        hand_b = Hand([
            Card(CardSuit.HEART, 2),
            Card(CardSuit.SPADE, 3),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.DIAMOND, 2),
            Card(CardSuit.HEART, 3)
        ])

        self.assertTrue(hand_a > hand_b)

    def test_three_of_a_kind_tie(self):
        hand_a = Hand([
            Card(CardSuit.HEART, 4),
            Card(CardSuit.SPADE, 3),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.DIAMOND, 5),
            Card(CardSuit.HEART, 4)
        ])

        hand_b = Hand([
            Card(CardSuit.HEART, 2),
            Card(CardSuit.SPADE, 2),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.DIAMOND, 2),
            Card(CardSuit.HEART, 3)
        ])

        self.assertTrue(hand_a > hand_b)
    
    def test_flush_tie(self):
        hand_a = Hand([
            Card(CardSuit.HEART, 9),
            Card(CardSuit.HEART, 3),
            Card(CardSuit.HEART, 7),
            Card(CardSuit.HEART, 5),
            Card(CardSuit.HEART, 4)
        ])

        hand_b = Hand([
            Card(CardSuit.HEART, 7),
            Card(CardSuit.HEART, 1),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.HEART, 5),
            Card(CardSuit.HEART, 3)
        ])

        self.assertTrue(hand_a > hand_b)

    def test_straight_tie(self):
        hand_a = Hand([
            Card(CardSuit.HEART, 3),
            Card(CardSuit.SPADE, 5),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.DIAMOND, 7),
            Card(CardSuit.HEART, 6)
        ])

        hand_b = Hand([
            Card(CardSuit.HEART, 1),
            Card(CardSuit.SPADE, 3),
            Card(CardSuit.HEART, 4),
            Card(CardSuit.DIAMOND, 5),
            Card(CardSuit.HEART, 2)
        ])

        self.assertTrue(hand_a > hand_b)
