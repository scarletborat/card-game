from card import Card
from random import sample

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

    def init_deck(self, deck_type) -> None:
       card_range = values_per_suit[deck_type]

       for suit in suits.keys():
          for value in range(card_range[0], card_range[1] + 1):
             card = Card(suit=suit, value=value)
             self.deck.append(card)
    
    def get_cards(self, number_of_cards):
      random_cards = sample(self.deck, number_of_cards) if len(self.deck) > number_of_cards else self.deck[:]
        
      for card in random_cards:
        self.deck.remove(card)

      return random_cards 
    
    def get_len(self):
       return len(self.deck)
