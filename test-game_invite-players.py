import unittest
from unittest import TestCase
from unittest.mock import patch
from io import StringIO
import sys

from game import Game

class InvitePlayers(TestCase):
    @patch('builtins.input', side_effect=['John', 'Jane', 'start'])
    def test_positive_case(self, mock_input):
        game = Game()
        players = game.invite_players()
        self.assertEqual(players, ['John', 'Jane'])

    @patch('builtins.input', side_effect=['John', 'start', 'q'])
    def test_two_user_min(self, mock_input):
        game = Game()
        expected_output = "Must be at least 2 players in the game\n\n"

        captured_output = StringIO()
        sys.stdout = captured_output

        game.invite_players()
        actual_output = captured_output.getvalue()

        sys.stdout = sys.__stdout__

        self.assertEqual(actual_output, expected_output)

    @patch('builtins.input', side_effect=['John', 'Anton', 'q'])
    def test_quit(self, mock_input):
        game = Game()
        players = game.invite_players()
        print(f"Players: {players}")
        self.assertEqual(players, None)

    

if __name__ == '__main__':
    unittest.main()