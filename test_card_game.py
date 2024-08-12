import unittest
from card_game import Card, CardGame


class TestCardGame(unittest.TestCase):
    def setUp(self):
        self.game = CardGame()

    def test_create_deck(self):
        self.game.create_deck()
        self.assertEqual(len(self.game.deck), 52)  # Check if the deck has 52 cards

    def test_deal(self):
        self.game.create_deck()
        self.game.deal("Player 1", 5)
        self.assertEqual(len(self.game.deck), 47)  # Check if 5 cards were removed from the deck
        self.assertEqual(len(self.game.hands["Player 1"]), 5)  # Check if 5 cards were added to the player's hand

    def test_deal_all(self):
        self.game.create_deck()
        self.game.hands = {"Player 1": [], "Player 2": []}
        self.game.deal_all(7)
        self.assertEqual(len(self.game.deck), 38)  # Check if 14 cards were removed from the deck
        for player, hand in self.game.hands.items():
            self.assertEqual(len(hand), 7)  # Check if 7 cards were added to each player's hand

    def test_discard(self):
        self.game.create_deck()
        self.game.deal("Player 1", 3)
        card_to_discard = self.game.hands["Player 1"][0]
        discarded_value = card_to_discard.value
        discarded_suit = card_to_discard.suit
        self.game.discard("Player 1", card_to_discard)
        self.assertEqual(len(self.game.hands["Player 1"]), 2)  # Check if the discarded card was removed from the player's hand
        self.assertEqual(self.game.deck[-1].suit, discarded_suit)
        self.assertEqual(self.game.deck[-1].value, discarded_value)

    def test_discard_all(self):
        self.game.create_deck()
        self.game.hands = {"Player 1": [], "Player 2": []}
        self.game.deal_all(7)
        self.game.discard_all()
        self.assertEqual(len(self.game.deck), 52)
        # Check if each hand is empty
        for hand in self.game.hands.values():
            self.assertEqual(len(hand), 0)

    def test_compare(self):
        card1 = Card('H', 5)
        card2 = Card('H', 5)
        card3 = Card('S', 5)
        card4 = Card('S', 7)
        self.assertGreater(card4, card3)
        self.assertLess(card2, card3)
        self.assertEqual(card1, card2)


if __name__ == '__main__':
    unittest.main()