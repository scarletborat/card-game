import unittest
from unittest import TestCase
from unittest.mock import patch
from io import StringIO
import sys

from card import Card
from game import Game

class BasicStub(Game):
  def invite_players(self):
      return ['John', 'Jane']
      
class GameCircle(TestCase):
    def test_user_lost(self):
      class Stub(BasicStub):
         def small_circle(self, attackers, attacker_index, defender):
          attacker = attackers[attacker_index]
          attacker_cards = [attacker.place_card(f"{card.get_suit()}:{card.get_value()}") for card in attacker.get_cards()]
          defender.draw_cards(attacker_cards)
          return 1
      
      game = Stub()
      game.deck.deck = []

      player_cards = [
        [Card(suit='heart', value=6), Card(suit='heart', value=7)],
        [Card(suit='diamond', value=6), Card(suit='diamond', value=7), Card(suit='diamond', value=8)]
      ]

      for i, player in enumerate(game.players):
         player.cards = player_cards[i]

      captured_output = StringIO()
      sys.stdout = captured_output

      game.game_circle()
      actual_output = captured_output.getvalue()
      sys.stdout = sys.__stdout__

      self.assertEqual(actual_output, f"Game over! {game.players[1].get_name().title()} you lost\n")

    def test_draw(self):
      class Stub(BasicStub):
        def small_circle(self, attackers, attacker_index, defender):
          for attacker in attackers:
            attacker.cards = []
          defender.cards = []
          return 0

      game = Stub()
      game.deck.deck = []

      player_cards = [
        [Card(suit='heart', value=6), Card(suit='diamond', value=7)],
        [Card(suit='heart', value=7), Card(suit='diamond', value=8)]
      ]

      for i, player in enumerate(game.players):
         player.cards = player_cards[i]

      captured_output = StringIO()
      sys.stdout = captured_output

      game.game_circle()
      actual_output = captured_output.getvalue()
      sys.stdout = sys.__stdout__

      self.assertEqual(actual_output, "Game over! Draw!\n")

if __name__ == '__main__':
    unittest.main()