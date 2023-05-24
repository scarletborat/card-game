from player import Player
from deck import Deck

def cycle(list, start_index, callback):
  index = start_index
  counter = 0
  length = len(list)

  while counter < length:
      callback(list[index])
      index = (index + 1) % length
      counter += 1

def cards_representation(cards):
  cards_representation = [card.get_suit()+':'+str(card.get_value())+' ' for card in cards]
  cards_representation = ''.join(cards_representation)
  return cards_representation

class Game:
  def __init__(self, number_of_players) -> None:
    self.number_of_players = number_of_players
    self.deck = Deck()
    self.discard_pile = []

    self.players = []
    self.exited_players = []

    self.attacker = 0
    self.defender = 1

    trump_card = self.deck.get_trump()
    min_trump = 14
    min_trump_player_i = 0

    names = ['Anton', 'Sveta', 'Vitalik', 'Beglec']
    for i in range(self.number_of_players):
      name = names[i] #input(f"Input name of the {i} player\n")
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

  def draw_cards(self, players):
    for player in players:
      cards_number = self.deck.cards_per_player() - player.crads_number()
      cards = self.deck.get_cards(cards_number)
      player.draw_cards(cards)

  def small_circle(self, attackers, attacker_index, defender):
    table_cards = []
    passes = 0
    attacker = attackers[attacker_index]

    print(f'Trump is {self.deck.get_trump()}')

    print(f"{attacker.get_name().title()} you are attacker\n")
    print("You cards are:\n")
    print(cards_representation(attacker.get_cards())+'\n')

    suit_value = input('Enter the card\n')
    card = attacker.place_card(suit_value)
    table_cards.insert(0, card)

    while passes < len(attackers):
      if not passes:
        print(f"{defender.get_name().title()} you are defender\n")
        print("You cards are:\n")
        print(cards_representation(defender.get_cards())+'\n')
        suit_value = input('Enter the card\n')
        print(f"Defender type {suit_value}")

        if suit_value != 'take':
          card = defender.place_card(suit_value)
          table_cards.insert(0, card)
        else:
          defender.draw_cards(table_cards)
          return 1

      attacker_index = (attacker_index + 1) % len(attackers)
      attacker = attackers[attacker_index]

      print(f"{attacker.get_name().title()} you are attacker\n")
      print("You cards are:\n")
      print(cards_representation(attacker.get_cards())+'\n')

      suit_value = input('Enter the card\n')
      if suit_value != 'continue':
        card = defender.place_card(suit_value)
        table_cards.insert(0, card)
        passes = 0
      else:
        passes += 1

    self.discard_pile += table_cards
    return 0

  # def attack(self):
  #   table_cards = []
  #   attacker = self.players[self.attacker]

  #   print(f"{attacker.get_name().title()} is your turn\n")
  #   print("You cards are:\n")
  #   print(cards_representation(attacker.get_cards())+'\n')

  #   suit_value = None
  #   while attacker.card_index(suit_value) == -1:
  #     suit_value = input('Enter the card\n')
  #   attacker_card = attacker.place_card(suit_value)
  #   table_cards.insert(0, attacker_card)
    
  #   print('Cards on the table:\n')
  #   print(cards_representation(table_cards)+'\n')

  #   print("You cards are:\n")
  #   print(cards_representation(attacker.get_cards())+'\n')

  #   defender = self.players[self.defender]

  #   print(f"{defender.get_name().title()} is your turn\n")
  #   print("You cards are:\n")
  #   print(cards_representation(defender.get_cards())+'\n')


  #   suit_value = None
  #   while defender.card_index(suit_value) == -1:
  #     suit_value = input('Enter the card\n')
    
  #   defender_card = defender.get_card(suit_value)

    
