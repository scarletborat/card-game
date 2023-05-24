import re

def one_str_occurrence(string, substring):
    pattern = r'^[^{0}]*{0}[^{0}]*$'.format(re.escape(substring))
    matches = re.findall(pattern, string)
    return len(matches) == 1

class Player:
  def __init__(self, name) -> None:
    self.name = name
    self.cards = []
    self.trump_card = None
    self.queue_position = None

  def draw_cards(self, cards):
    for card in cards:
      self.cards.append(card)

  def get_cards(self):
    return self.cards

  def cards_number(self):
    return len(self.cards)

  def set_trump_card(self, trump_card):
    self.trump_card = trump_card

  def set_queue_position(self, num):
    self.queue_position = num

  def get_queue_position(self):
    return self.queue_position

  def get_min_trump(self):
    trumps = [card for card in self.cards if card.get_suit() == self.trump_card]
    return min(trumps, key=lambda x: x.get_value()).get_value() if len(trumps) else None

  def get_name(self):
    return self.name

  def get_card(self, suit_value):
    index = self.card_index(suit_value)
    if index == -1:
      return False
    
    return self.cards[index]

  def place_card(self, suit_value):
    index = self.card_index(suit_value)
    if index == -1:
      return False
    
    card = self.cards[index]
    self.cards.remove(card)

    return card

  def card_index(self, suit_value):
    if not suit_value or not one_str_occurrence(suit_value, ':'):
      return -1

    suit, value = suit_value.split(':')
    value = int(value)
    index = -1
    
    for i, card in enumerate(self.cards):
      if card.get_suit() == suit and card.get_value() == value:
        index = i
        break
    return index

  def can_tosse(self, suit_value, table_cards): #TODO remove
    index = self.card_index(suit_value)
    if index == -1:
      return False
    return bool([c for c in table_cards if c.get_value() == self.cards[index].get_value()])
