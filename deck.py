from card import Card
from random import sample, shuffle

deck_36 = 36
deck_52 = 52

suits = {
  'heart': 'heart',
  'diamond': 'diamond',
  'club': 'club',
  'spades': 'spades'
}

values_per_suit = {
   deck_36: [6, 14],
   deck_52: [2, 14]
}

class Deck:
    def __init__(self, deck_type = 36):
      self.deck_type = deck_type
      self.deck = []
      self.init_deck(self.deck_type)
      self.trump = None

    def init_deck(self, deck_type) -> None:
      card_range = values_per_suit[deck_type]

      for suit in suits.keys():
        for value in range(card_range[0], card_range[1] + 1):
            card = Card(suit=suit, value=value)
            self.deck.append(card)
      
      shuffle(self.deck)

    def get_cards(self, number_of_cards):
      cards = self.deck[:number_of_cards]
        
      for card in cards:
        self.deck.remove(card)

      return cards 

    def get_len(self):
       return len(self.deck)

    def get_trump(self):
      if not self.trump:
        self.trump = self.deck[-1].get_suit()
      return self.trump

    def cards_per_player(self):
       return 6