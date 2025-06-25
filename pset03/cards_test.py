import unittest
from cards import (
    Card, standard_deck, shuffled_deck, deal_one_five_card_hand,
    deal, poker_classification)


# helper function to create a card from string like 'AH' or '10S'
def make_card(description):
    if len(description) != 2:
        return None
    rank_str = description[:-1]
    suit_str = description[-1].upper()
    if suit_str not in "SHDC" or rank_str not in "A23456789TJQK":
        return None
    return Card(suit=suit_str, rank="A23456789TJQK".index(rank_str) + 1)


# helper function to create a hand from string like 'AH 10S 5D'
def make_hand(description):
    return {make_card(card) for card in description.split()}


# tests for card class and functions
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

    def test_deal_invalid_inputs(self):
        with self.assertRaises(TypeError):
            deal("two", 5)
        with self.assertRaises(TypeError):
            deal(2, "five")
        with self.assertRaises(ValueError):
            deal(0, 5)
        with self.assertRaises(ValueError):
            deal(2, -5)
        with self.assertRaises(ValueError):
            deal(11, 5)

    def test_deal_valid_inputs(self):
        hands = deal(6, 7)
        self.assertIsInstance(hands, list)
        self.assertEqual(len(hands), 6)
        for hand in hands:
            self.assertIsInstance(hand, set)
            self.assertEqual(len(hand), 7)
            self.assertTrue(all(isinstance(card, Card) for card in hand))
        # check that all cards are unique across both hands
        all_cards = set().union(*hands)
        self.assertEqual(len(all_cards), 42)

    def test_poker_classification(self):
        tests = [
            (make_hand("2H 3H 4H 5H 6H"), "Straight Flush"),
            (make_hand("JH TH QH KH AH"), "Royal Flush"),
            (make_hand("QS TS AS KS JS"), "Royal Flush"),
            (make_hand("2H 2D 3H 3D 4H"), "Two Pair"),
            (make_hand("KD 2D 3H 3D KH"), "Two Pair"),
            (make_hand("2H 2D 2C 3H 4H"), "Three of a Kind"),
            (make_hand("2S 3H 4H 5H 7H"), "High Card"),
            (make_hand("2S 3H 4H 5H KH"), "High Card"),
            (make_hand("2H 3H 4H 5H 6D"), "Straight"),
            (make_hand("2H 3H 4H 5H AD"), "Straight"),
            (make_hand("KH QC JC TC AD"), "Straight"),
            (make_hand("2C TC 4C 5C 6C"), "Flush"),
            (make_hand("2H 2D 2C 2S 3H"), "Four of a Kind"),
            (make_hand("2H AD AC AS AH"), "Four of a Kind"),
        ]
        for hand, expected in tests:
            with self.subTest(hand=hand):
                self.assertEqual(poker_classification(hand), expected)
