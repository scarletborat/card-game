from player import Player
from deck import Deck

from utils import one_str_occurrence, text_bold

def cycle(list, start_index, callback):
  index = start_index
  counter = 0
  length = len(list)

  while counter < length:
      callback(list[index])
      index = (index + 1) % length
      counter += 1

def next(index, number):
  return index % number

def cards_representation(cards, highlight_first_card = False):
  cards = list(cards)
  cards_representation = []
  if highlight_first_card:
    card = cards[0]
    del cards[0]
    cards_representation = [text_bold(card.get_suit()+':'+str(card.get_value())) + ' ']
  cards_representation += [card.get_suit()+':'+str(card.get_value())+' ' for card in cards]
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
  print(f"{text_bold(player.get_name().title())} - {text_bold(role)}, your cards:")
  print(cards_representation(player.get_cards())+'\n')

def show_table_cards(cards):
  print("Cards on the table are:")
  print(cards_representation(cards, True)+'\n')

class Game:
  def __init__(self) -> None:
    self.deck = Deck()
    self.discard_pile = []

    self.players = []
    self.exited_players = []

  def start(self):
    players_names = self.invite_players()
    self.init_and_arrange_first_turn_order(players_names)
    self.game_circle()

  def init_and_arrange_first_turn_order(self, players_names):
    min_trump = 14
    min_trump_player_i = 0

    for i, name in enumerate(players_names):
      player = Player(name=name)

      player_cards = self.deck.get_cards(6)
      player.draw_cards(player_cards)

      player.set_trump_card(self.deck.get_trump())
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
      player_name = input_value(f"Please input {player_num} player name\n")
      if player_name == 'q':
        return None
      elif player_name == 'start':
        if len(players) < 2:
          print("Must be at least 2 players in the game\n")
          continue
        else:
          return players
      else:
        players.append(player_name)
        player_num += 1

  def draw_cards(self, players):
    for player in players:
      cards_number = self.deck.cards_per_player() - player.cards_number()
      if cards_number <= 0:
        return
      cards = self.deck.get_cards(cards_number)
      player.draw_cards(cards)

  def init_turn(self, message, player):
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
      if card.get_suit() == top_table_card.get_suit() and card.get_value() > top_table_card.get_value():
        return player.place_card(value)
      if self.deck.get_trump() != top_table_card.get_suit() and card.get_suit() == self.deck.get_trump():
        return player.place_card(value)

  def discard_turn(self, message, player, table_cards):
    while True:
      value = input_value(message)
      if value == 'c' or value == 'continue':
        return False
      if not player_has_card(value, player):
        continue
      card = player.get_card(value)
      matches = [table_card for table_card in table_cards if table_card.get_value() == card.get_value()]
      if matches:
        return player.place_card(value)

  def small_circle(self, attackers, attacker, defender):
    table_cards = []
    passes = 0

    print(f"Trump are {text_bold(self.deck.get_trump())}\n")
    player_notification(attacker, 'attacker')

    card = self.init_turn('Enter the card\n', attacker)
    table_cards.insert(0, card)
    show_table_cards(table_cards)

    while True:
      if passes == 0:
        player_notification(defender, 'defender')
        card = self.defender_turn('Enter the card\n', defender, table_cards[0])

        if card:
          table_cards.insert(0, card)
          show_table_cards(table_cards)
        else:
          defender.draw_cards(table_cards)
          return 1

      attacker = attackers[next(attackers.index(attacker) + 1, len(attackers))]
      player_notification(attacker, 'attacker')
      card = self.discard_turn('Enter the card\n', attacker, table_cards)

      if card:
        passes = 0
        table_cards.insert(0, card)
        show_table_cards(table_cards)
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
    attacker = attackers[attacker_index]

    while True:
      took = self.small_circle(attackers, attacker, defender)

      if self.deck.get_len():
        self.draw_cards(players)

      i_players_with_cards = [i for i, player in enumerate(players) if player.cards_number()]
      length = len(i_players_with_cards)

      if length < 2:
        if length == 1:
          name = text_bold(players[i_players_with_cards[0]].get_name().title())
          print(f"Game over!\n{name} you lost")
        elif length == 0:
          print(f"Game over! Draw!")
        break

      if not took and defender.cards_number():
        attacker = defender
      else:
        attacker_index = (defender_index + 1) % len(players)
        while not players[attacker_index].cards_number():
          attacker_index = (attacker_index + 1) % len(players)
        attacker = players[attacker_index]

      attackers = [players[i] for i in i_players_with_cards]
      attacker_index = attackers.index(attacker)
      defender_index = (attacker_index + 1) % len(attackers)
      defender = attackers[defender_index]
      del attackers[defender_index]
