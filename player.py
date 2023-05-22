class Player:
  def __init__(self, name) -> None:
    self.name = name
    self.cards = []

  def draw_cards(self, cards):
    for card in cards:
      self.cards.append(card)

  def get_cards(self):
    return self.cards
  
  def get_number_of_cards(self):
    return len(self.cards)