import unittest
from card import (
    Card,
    standard_deck,
    shuffled_deck,
    deal_one_five_card_hand,
    deal_two_five_card_hands,
)


class TestCard(unittest.TestCase):
    def test_valid_cards(self):
        self.assertEqual(str(Card(suit="H", rank=10)), "10♥")
        self.assertEqual(str(Card(suit="S", rank=1)), "A♠")
        self.assertEqual(str(Card(suit="D", rank=11)), "J♦")
        self.assertEqual(str(Card(suit="C", rank=12)), "Q♣")
        self.assertEqual(str(Card(suit="H", rank=13)), "K♥")
        self.assertEqual(str(Card(suit="S", rank=5)), "5♠")
        self.assertEqual(str(Card(suit="D", rank=3)), "3♦")
        self.assertEqual(str(Card(suit="C", rank=2)), "2♣")

    def test_invalid_suit(self):
        with self.assertRaises(ValueError):
            Card(suit="X", rank=5)
        with self.assertRaises(ValueError):
            Card(suit="SPADES", rank=10)

    def test_invalid_rank(self):
        with self.assertRaises(ValueError):
            Card(suit="S", rank=14)
        with self.assertRaises(ValueError):
            Card(suit="D", rank=0)
        with self.assertRaises(ValueError):
            Card(suit="D", rank=3.5)
        with self.assertRaises(ValueError):
            Card(suit="D", rank="10")

    def test_cards_are_truly_immutable(self):
        card = Card(suit="H", rank=10)
        with self.assertRaises(AttributeError):
            card.suit = "S"
        with self.assertRaises(AttributeError):
            card.rank = 5
        with self.assertRaises(AttributeError):
            card.dog = "dog"

    def test_standard_deck(self):
        deck = standard_deck()
        self.assertIsInstance(deck, list)
        self.assertEqual(len(deck), 52)
        self.assertTrue(all(isinstance(card, Card) for card in deck))
        deck_as_string = ''.join(str(card) for card in deck)
        self.assertEqual(deck_as_string,
                         "A♠2♠3♠4♠5♠6♠7♠8♠9♠10♠J♠Q♠K♠"
                         "A♥2♥3♥4♥5♥6♥7♥8♥9♥10♥J♥Q♥K♥"
                         "A♦2♦3♦4♦5♦6♦7♦8♦9♦10♦J♦Q♦K♦"
                         "A♣2♣3♣4♣5♣6♣7♣8♣9♣10♣J♣Q♣K♣")

    def test_shuffled_deck(self):
        deck = standard_deck()
        self.assertIsInstance(deck, list)
        self.assertEqual(len(deck), 52)
        shuffled = shuffled_deck()
        self.assertIsInstance(shuffled, list)
        self.assertEqual(len(shuffled), 52)
        for suit in "SHDC":
            for rank in range(1, 14):
                self.assertIn(Card(suit, rank), shuffled)

    def test_deal_one_five_card_hand(self):
        hand = deal_one_five_card_hand()
        self.assertIsInstance(hand, set)
        self.assertEqual(len(hand), 5)
        self.assertTrue(all(isinstance(card, Card) for card in hand))

    def test_deal_two_five_card_hands(self):
        hand1, hand2 = deal_two_five_card_hands()
        self.assertIsInstance(hand1, set)
        self.assertIsInstance(hand2, set)
        self.assertEqual(len(hand1), 5)
        self.assertEqual(len(hand2), 5)
        self.assertTrue(all(isinstance(card, Card) for card in hand1))
        self.assertTrue(all(isinstance(card, Card) for card in hand2))
        self.assertTrue(hand1.isdisjoint(hand2))  # hands should not overlap


if __name__ == "__main__":
    unittest.main()
