"""
The Triple Triad card game, of Final Fantasy VIII, now playable in your terminal.
"""

import random
import sys
import string
from termcolor import colored

BLACK, RED, GREEN, YELLOW, cyan, MAGENTA, CYAN, WHITE = range(8)

# --------------- MODELS ---------------

class Card(object):
	def __init__(self, top, right, bottom, left, color):
		self.top = top
		self.right = right
		self.bottom = bottom
		self.left = left
		self.color = color

	def flip(self):
		if self.color == "cyan":
			self.color = "red"
		else:
			self.color = "cyan"

# --------------- Card interaction + game logic ---------------

def calculate_scores(p1_hand, p2_hand, board):
	p1_score = 0
	p2_score = 0
	for card in (p1_hand + p2_hand + [x for sublist in board for x in sublist]):
		if card is not None:
			if card.color == "cyan":
				p1_score = p1_score + 1
			if card.color == "red":
				p2_score = p2_score + 1
	print "Player 1: " + str(p1_score)
	print "Player 2: " + str(p2_score)

def place(card, location, board, hand):
	""" Place Card card in (row, column) location """
	row = location / 3
	column = location % 3

	board[row][column] = card
	hand.remove(card)

	if not (row-1 < 0):
		if board[row-1][column] is not None:
			if board[row-1][column].bottom < board[row][column].top:
				board[row-1][column].flip()

	if not (column+1 > 2):
		if board[row][column+1] is not None:
			if board[row][column+1].left < board[row][column].right:
				board[row][column+1].flip()

	if not (row+1 > 2):
		if board[row+1][column] is not None:
			if board[row+1][column].top < board[row][column].bottom:
				board[row+1][column].flip()

	if not (column-1 < 0):
		if board[row][column-1] is not None:
			if board[row][column-1].right < board[row][column].left:
				board[row][column-1].flip()

def load_deck(file):
	deck = []
	for line in open(file):
		if '#' not in line:
			card_descriptor = [int(x) for x in line.split(',')]
			card_descriptor.append(None)
			deck.append(Card(*card_descriptor))
	return deck

def load_hand(color, deck):
	hand = []
	for i in range(0,5):
		hand.append(deck.pop(random.randrange(len(deck))))
	for card in hand:
		card.color = color
	return hand

def prompt_location_choice(board):
	selection = raw_input("Place card where? ")
	return ord(selection.strip()) - 97

def prompt_card_choice(hand):
	print "Your hand: "
	for card, letter in zip(hand, string.ascii_lowercase):
		print letter + ". " + str([card.top, card.left, card.right, card.bottom])
	selection = raw_input("Select your card: ")
	for card, letter in zip(hand, string.ascii_lowercase):
		if letter == selection:
			return card

# --------------- UI, inasmuch as this counts as UI ---------------

def print_board(board):
	for i in range(0,3):
		_print_boundary()
		_print_toprow(board[i][0], board[i][1], board[i][2])
		_print_midrow(board[i][0], board[i][1], board[i][2], i)
		_print_bottomrow(board[i][0], board[i][1], board[i][2])
	_print_boundary()

def _print_boundary():
	print "-------------------------"

def _print_toprow(left, middle, right):
	display = []
	print "|",
	for card in [left, middle, right]:
		if card is not None:
			print " ",
			print colored(str(card.top), card.color),
			print "  |",
		else:
			print "      |",
	print ""

def _print_bottomrow(left, middle, right):
	display = []
	print "|",
	for card in [left, middle, right]:
		if card is not None:
			print " ",
			print colored(str(card.bottom), card.color),
			print "  |",
		else:
			print "      |",
	print ""

def _print_midrow(left, middle, right, letter_num):
	letter_num = (letter_num * 3) + 97
	display = []
	print "|",
	for card in [left, middle, right]:
		if card is not None:
			print colored(str(card.left), card.color),
			print " ",
			print colored(str(card.right), card.color),
			print "|",
		else:
			print "  " + chr(letter_num) + "   |",
		letter_num = letter_num + 1
	print ""

# --------------- Main game loop ---------------

def main():
	""" Core game loop """
	print "WELCOME TO TRIPLE TRIAD"
	print "Insert shuffle or boogie theme here"
	deck = load_deck('cards.txt')
	p1_hand = load_hand("cyan", deck)
	p2_hand = load_hand("red", deck)
	board = []
	for i in range(0,3):
		board.append([None, None, None])
	game = True
	print_board(board)
	turn = "human"
	while game:
		if turn == "human":
			card = prompt_card_choice(p1_hand)
			location = prompt_location_choice(board)
			place(card, location, board, p1_hand)
			print ""
			print_board(board)
			winning = calculate_scores(p1_hand, p2_hand, board)
			print ""
			turn = "computer"

		else:
			card = random.choice(p2_hand)
			location = random.choice([i for i, j in enumerate([x for sublist in board for x in sublist]) if j is None])
			place(card, location, board, p2_hand)
			print_board(board)
			winning = calculate_scores(p1_hand, p2_hand, board)
			turn = "human"

		if None not in [item for sublist in board for item in sublist]:
			game = False

main()