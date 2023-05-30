from player import Player
from deck import Deck

from utils import one_str_occurrence

def cycle(list, start_index, callback):
  index = start_index
  counter = 0
  length = len(list)

  while counter < length:
      callback(list[index])
      index = (index + 1) % length
      counter += 1

def next(number, i):
  return (number + i) % number

def cards_representation(cards):
  cards_representation = [card.get_suit()+':'+str(card.get_value())+' ' for card in cards]
  cards_representation = ''.join(cards_representation)
  return cards_representation

def input_value(message):
  val = None
  while not val:
    val = input(message)
  return val

def player_has_card(suit_value, player):
  if one_str_occurrence(suit_value, ':'):
    index = player.card_index(suit_value)
    return index != -1
  return False

def player_notification(player, role):
  print(f"{player.get_name().title()} you are {role}\n")
  print("You cards are:\n")
  print(cards_representation(player.get_cards())+'\n')

class Game:
  def __init__(self) -> None:
    self.deck = Deck()
    self.discard_pile = []

    self.players = []
    self.exited_players = []

    self.attacker = 0
    self.defender = 1

    trump_card = self.deck.get_trump()
    min_trump = 14
    min_trump_player_i = 0

    players_names = self.invite_players()

    for i, name in enumerate(players_names):
      player = Player(name=name)

      player_cards = self.deck.get_cards(6)
      player.draw_cards(player_cards)

      player.set_trump_card(trump_card)
      player_min_trump = player.get_min_trump()

      if player_min_trump and player_min_trump < min_trump:
        min_trump = player_min_trump
        min_trump_player_i = i

      self.players.append(player)

    self.players = self.players[min_trump_player_i:] + self.players[:min_trump_player_i]

  def invite_players(self):
    players = []
    player_num = 1
    while True:
      player_name = input(f"Please input {player_num} player name")
      if player_name == 'q':
        return None
      elif player_name == 'start':
        if len(players) < 2:
          print("Must be at least 2 players in the game")
        else:
          return players
      else:
        players.append(player_name)

  def draw_cards(self, players):
    for player in players:
      cards_number = self.deck.cards_per_player() - player.crads_number()
      cards = self.deck.get_cards(cards_number)
      player.draw_cards(cards)

  def init_turn(message, player):
    while True:
      suit_value = input_value(message)
      if player_has_card(suit_value, player):
        return player.place_card(suit_value)

  def defender_turn(self, message, player, top_table_card):
    while True:
      value = input_value(message)
      if value == 't' or value == 'take':
        return False
      if not player_has_card(value, player):
        continue
      card = player.get_card(value)
      if card.get_suit() == top_table_card.get_suit() and card.get_value > top_table_card.get_value():
        return player.place_card(value)
      if self.deck.get_trump() != top_table_card.get_suit() and card.get_suit() == self.deck.get_trump():
        return player.place_card(value)

  def discard_turn(self, message, player, top_table_card):
    while True:
      value = input_value(message)
      if value == 'c' or value == 'continue':
        return False
      if not player_has_card(value, player):
        continue
      card = player.get_card(value)
      if card.get_suit() == top_table_card.get_suit():
        return player.place_card(value)

  def small_circle(self, attackers, attacker_index, defender):
    table_cards = []
    passes = 0
    attacker = attackers[attacker_index]

    print(f'Trump is {self.deck.get_trump()}')
    player_notification(attacker, 'attacker')

    card = self.init_turn('Enter the card\n', attacker)
    table_cards.insert(0, card)

    while True:
      player_notification(defender, 'defender')
      card = self.defender_turn('Enter the card\n', defender, table_cards[0])

      if card:
        table_cards.insert(0, card)
      else:
        defender.draw_cards(table_cards)
        return 1

      attacker = attackers[next(len(attackers), attacker_index + 1)]
      player_notification(attacker, 'attacker')
      card = self.discard_turn('Enter the card\n', defender, table_cards[0])

      if card:
        passes = 0
        table_cards.insert(0, card)
      else:
        passes += 1

      if passes >= len(attackers) or not defender.cards_number():
        self.discard_pile += table_cards
        return 0

  def game_circle(self):
    players = list(self.players)
    
    attacker_index = 0
    defender_index = 1
    defender = players[defender_index]
    attackers = []
    for i, attacker in enumerate(players):
      if i != defender_index:
        attackers.append(attacker)

    while True:
      took = self.small_circle(attackers, attacker_index, defender)

      if self.deck.get_len():
        self.draw_cards(players)

      players = [player for player in players if player.cards_number()]

      if len(players) < 2:
        if len(players) == 1:
          print(f"Game over! {players[0].get_name().title()} you lost")
        elif len(players) == 0:
          print(f"Game over! Draw!")
        break

      attacker_index = next(len(players), attacker_index + 1 + took)
      defender_index = next(len(players), attacker_index + 1)
      attackers = list(players)
      defender = attackers[defender_index]
      del attackers[defender_index]
