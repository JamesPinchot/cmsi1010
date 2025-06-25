from dataclasses import dataclass
from random import shuffle


# class for a single card
@dataclass(frozen=True)
class Card:
    suit: str
    rank: int

    def __post_init__(self):
        if self.suit not in ("S", "H", "D", "C"):
            raise ValueError("suit must be one of 'S', 'H', 'D', 'C'")
        if self.rank not in range(1, 14):
            raise ValueError("rank must be an integer between 1 and 13")

    def __str__(self):
        suit_str = {"S": "♠", "H": "♥", "D": "♦", "C": "♣"}[self.suit]
        rank_str = {1: "A", 11: "J", 12: "Q", 13: "K"}.get(
            self.rank, str(self.rank))
        return f"{rank_str}{suit_str}"


# make a standard deck
def standard_deck():
    return [Card(suit, rank) for suit in "SHDC" for rank in range(1, 14)]


# make a shuffled deck
def shuffled_deck():
    cards = standard_deck()
    shuffle(cards)
    return cards


# deal one hand of 5 cards
def deal_one_five_card_hand():
    deck = shuffled_deck()
    return set(deck[:5])


# deal multiple hands
def deal(number_of_hands, cards_per_hand):
    if not isinstance(number_of_hands, int) or not isinstance(cards_per_hand, int):
        raise TypeError("number_of_hands and cards_per_hand must be integers")
    if number_of_hands <= 0 or cards_per_hand <= 0:
        raise ValueError("number_of_hands and cards_per_hand must be positive")
    if number_of_hands * cards_per_hand > 52:
        raise ValueError("not enough cards to deal")

    deck = shuffled_deck()
    hands = []
    for i in range(number_of_hands):
        hand = set(deck[i * cards_per_hand : (i + 1) * cards_per_hand])
        hands.append(hand)
    return hands


# check poker hand classification
def poker_classification(hand):
    if not isinstance(hand, set):
        raise TypeError("the hand must be a set of Card objects")
    if len(hand) != 5:
        raise ValueError("the hand must contain exactly 5 cards")
    if not all(isinstance(card, Card) for card in hand):
        raise TypeError("all elements in the hand must be Card objects")

    hand = sorted(hand, key=lambda card: card.rank)

    is_flush = all(card.suit == hand[0].suit for card in hand)

    ranks = [card.rank for card in hand]
    is_broadway_straight = (ranks == [1, 10, 11, 12, 13])
    is_lower_straight = all(
        ranks[i] == ranks[i-1]+1 for i in range(1, len(ranks)))
    is_straight = is_broadway_straight or is_lower_straight

    rank_counts = {}
    for card in hand:
        rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1
    counts = sorted(rank_counts.values(), reverse=True)

    if is_flush and is_broadway_straight:
        return "Royal Flush"
    if is_flush and is_straight:
        return "Straight Flush"
    if counts == [4, 1]:
        return "Four of a Kind"
    if counts == [3, 2]:
        return "Full House"
    if is_flush:
        return "Flush"
    if is_straight:
        return "Straight"
    if counts == [3, 1, 1]:
        return "Three of a Kind"
    if counts == [2, 2, 1]:
        return "Two Pair"
    if counts == [2, 1, 1, 1]:
        return "One Pair"
    return "High Card"
