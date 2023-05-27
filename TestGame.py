import unittest
from unittest import TestCase
from unittest.mock import patch
from io import StringIO
from sys

from game import Game

class TestGame(TestCase):
    @patch('builtins.input', side_effect=['John', 'Jane', 'start'])
    def invite_players_positive_case(self, mock_input):
        game = Game()
        players = game.invite_players()
        self.assertEqual(players, ['John', 'Jane'])

if __name__ == '__main__':
    unittest.main()