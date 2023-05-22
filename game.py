from player import Player
from deck import Deck

class Game:
  def __init__(self, number_of_players) -> None:
    self.number_of_players = number_of_players
    self.players = []
    self.deck = Deck()

  def start_game(self):
    for i in range(self.number_of_players):
      name = input(f"Input name of the {i} player")
      player = Player(name=name)
      player_cards = self.deck.get_cards(6)
      player.draw_cards(player_cards)

  
      

