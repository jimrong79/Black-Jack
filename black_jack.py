import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King')
values = {'Ace': 11, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10 \
         ,'Queen': 10, 'King': 10}


class Card():
	"""docstring for Card"""
	def __init__(self, suit, rank):
		
		self.suit = suit
		self.rank = rank
	
	def __str__(self):
		return self.rank + " of " + self.suit


class Deck():
	
	def __init__(self):
		self.deck = []

		for suit in suits:
			for rank in ranks:
				self.deck.append(Card(suit,rank))

	def __str__(self):
		remaining_cards = ''
		for card in self.deck:
			remaining_cards += '\n' + card.__str__()
		return remaining_cards

	def shuffle(self):
		random.shuffle(self.deck)

	def deal(self):
		dealt = self.deck.pop()
		return dealt

	def remaining_num_cards(self):
		return len(self.deck)

test_deck = Deck()
test_deck.shuffle()

class Hand():
	
	def __init__(self):
		self.hand = []
		self.value = 0
		self.ace = 0

	def take_card(self, card):
		self.hand.append(card)
		self.value += values[card.rank]

		if card.rank == 'Ace':
			self.ace += 1

	def adjust_for_ace(self):
		while self.value > 21 and self.ace > 0:
			self.value -= 10
			self.ace -= 1


class Chips():

	def __init__(self, total = 100):
		self.total = total
		self.bet = 0

	def win_bet(self):
		self.total += self.bet

	def lose_bet(self):
		self.total -= self.bet

def place_bets(chips):
	
	while True:
		try:
			print ("You have: " + str(chips.total))
			chips.bet = int(input("How much you would like to bet? "))
		except:
			print ("Invalid! Please provide integer!")
		else:
			if chips.bet > chips.total:
				print("Sorry, you don't have enough chips! You have {} ".format(chips.total))
			else:
				break


def hit(deck, hand):
	dealt_card = deck.deal()
	hand.take_card(dealt_card)
	hand.adjust_for_ace()

def hit_or_stay():
	while True:
		try:
			decision = int(input("Please decide hit or stay! \
			\n 1. Hit! \
			\n 2. Stay! "))
		except:
			print ("Invalid!")
		else:
			if decision == 1:
				return True
			elif decision == 2:
				return False
			else:
				print("Invalid! please input only 1 or 2!")


#hit_or_stay()

def show_some(player, dealer):
	print ("Dealer's Hand: ")
	print (dealer.hand[1])
	print ('\n')
	print ("Player's Hand: ")
	for card in player.hand:
		print (card)
	print ("Player's Hand Total: ")
	print (player.value)


def show_all(player, dealer):
	print ("Dealer's Hand: ")
	for card in dealer.hand:
		print (card)
	print ("Player's Hand: ")
	for card in player.hand:
		print (card)	

def show_hand(hand):
	for card in hand.hand:
		print (card)

def bust_check(hand):
	if hand.value > 21:
		return True
	return False

def win_check(player_hand, dealer_hand):
	if player_hand.value > dealer_hand.value:
		return True
	else:
		return False

def push_check(player_hand, dealer_hand):
	if player_hand.value == dealer_hand.value:
		return True
	else:
		return False

def dealer_decision(deck, hand):
	while hand.value < 17:
		hit(deck, hand)
		print("Dealer's Hand: ")
		show_hand(hand)
		print("\n")

	return hand

def start_game():
	print("Welcome to Black Jack!")

	while True:
		try:
			starting_chips = int(input("How much you want to put in this game?"))
		except:
			print("Invalid!")
		else:
			if starting_chips <= 0:
				player_chips = Chips()
			else:
				player_chips = Chips(starting_chips)
			break

	playing = True

	while playing:
		print ("--------------------New Deck!---------------------")
		deck = Deck()
		deck.shuffle()
		
		while (deck.remaining_num_cards() > 50 and playing and player_chips.total > 0):
			if (deck.remaining_num_cards() < 52):
				cont = input("Continue Playing? Y/N")
				if cont[0].lower() == 'n':
					playing = False
					break

			place_bets(player_chips)

			player_hand = Hand()
			dealer_hand = Hand()

			hit(deck, player_hand)
			hit(deck, player_hand)
			hit(deck, dealer_hand)
			hit(deck, dealer_hand)
			
			show_some(player_hand, dealer_hand)

			while (player_hand.value < 21 and hit_or_stay()):
				hit(deck, player_hand)
				show_some(player_hand, dealer_hand)

			if (bust_check(player_hand)):
				print("You Bust!")
				player_chips.lose_bet()
				continue

			dealer_decision(deck, dealer_hand)

			if (bust_check(dealer_hand)):
				print ("Dealer Bust!")
				player_chips.win_bet()
				continue

			if (push_check(player_hand, dealer_hand)):
				show_all(player_hand, dealer_hand)
				print ("Push!")
				continue

			if (win_check(player_hand, dealer_hand)):
				show_all(player_hand, dealer_hand)
				print ("You Win!")
				player_chips.win_bet()
				continue
			else:
				show_all(player_hand, dealer_hand)
				print ("You Lose!")
				player_chips.lose_bet()
				continue

		if playing:
			cont = input("Continue Playing? Y/N")
			if cont[0].lower() == 'n':
				playing = False
				break

	print ("Thanks for Playing Black Jack! You're remaining chips: ")
	print (player_chips.total)


start_game()