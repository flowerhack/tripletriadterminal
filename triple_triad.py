"""
The Triple Triad card game, of Final Fantasy VIII, now playable in your terminal.
"""

import random
import sys
import string
import itertools
from termcolor import colored

# --------------- OBJECTS ---------------

class Game(object):
    def __init__(self, deck, num_players=2):
        """
        deck: list of Cards that Players can use to make their hands
        num_players: number of players in this game.  This is a small lie;
        at the moment >2 players is not supported.
        """
        self.board = Board()
        self.players = []
        self.players.append(Player("human", load_hand("cyan", deck)))
        self.players.append(Player("computer", load_hand("red", deck)))
        self.player_loop = itertools.cycle(self.players)

    def calculate_scores(self):
        p1_score = 0
        p2_score = 0
        for card in (self.players[0].hand + self.players[1].hand + self.board.flat_list()):
            if card is not None:
                if card.color == "cyan":
                    p1_score = p1_score + 1
                if card.color == "red":
                    p2_score = p2_score + 1
        print "Player 1: " + str(p1_score)
        print "Player 2: " + str(p2_score)

    def run(self):
        self.board.display()
        running = True
        while running:
            current_player = next(self.player_loop)
            if current_player.type == "human":
                card = prompt_card_choice(current_player.hand)
                location = prompt_location_choice(self.board)
                self.board.place(card, location)
                current_player.hand.remove(card)
                print ""
                self.board.display()
                self.calculate_scores()
                print ""

            else:
                # Computer opponents always place a random card in a random location as of now.
                card = random.choice(current_player.hand)
                location = random.choice([i for i, j in enumerate(self.board.flat_list()) if j is None])
                self.board.place(card, location)
                current_player.hand.remove(card)
                print ""
                self.board.display()
                self.calculate_scores()
                print ""

            if None not in self.board.flat_list():
                # All the board slots have been filled; end the game.
                running = False


class Player(object):
    def __init__(self, type, hand):
        self.type = type
        self.hand = hand


class Card(object):
    def __init__(self, top, right, bottom, left, color):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left
        self.color = color

    def flip(self):
        # If support for >2 players is added, will need support >2 colors
        if self.color == "cyan":
            self.color = "red"
        else:
            self.color = "cyan"

    def display(self):
        print "  -------"
        print "  |  " + str(self.top) + "  |"
        print "  | " + str(self.left) + " " + str(self.right) + " |"
        print "  |  " + str(self.bottom) + "  |"
        print "  -------"


class Board(object):
    def __init__(self, width=3, height=3):
        self.board = []
        for i in range(0, height):
            self.board.append([None for i in range(0, width)])
        self.width = width
        self.height = height

    def place(self, card, location):
        row = location / self.height
        column = location % self.width

        self.board[row][column] = card

        if row-1 >= 0:
            if self.board[row-1][column] is not None:
                if self.board[row-1][column].bottom < self.board[row][column].top:
                    if self.board[row-1][column].color != self.board[row][column].color:
                        self.board[row-1][column].flip()

        if column+1 < self.width:
            if self.board[row][column+1] is not None:
                if self.board[row][column+1].left < self.board[row][column].right:
                    if self.board[row][column+1].color != self.board[row][column].color:
                        self.board[row][column+1].flip()

        if row+1 < self.height:
            if self.board[row+1][column] is not None:
                if self.board[row+1][column].top < self.board[row][column].bottom:
                    if self.board[row+1][column].color != self.board[row][column].color:
                        self.board[row+1][column].flip()

        if column-1 >= 0:
            if self.board[row][column-1] is not None:
                if self.board[row][column-1].right < self.board[row][column].left:
                    if self.board[row][column-1].color != self.board[row][column].color:
                        self.board[row][column-1].flip()

    def flat_list(self):
        """
        Useful for giving us 'flat', 2D representations of the board,
        e.g. when we want to select a square on the board at random.
        """
        return [x for sublist in self.board for x in sublist]

    # UI functions for the board, inasmuch as this counts as UI...

    def display(self):
        for i in range(0, self.height):
            self._print_boundary()
            self._print_toprow(self.board[i])
            self._print_midrow(self.board[i], i)
            self._print_bottomrow(self.board[i])
        self._print_boundary()

    def _print_boundary(self):
        print "-------------------------"

    def _print_toprow(self, cards):
        display = []
        print "|",
        for card in cards:
            if card is not None:
                print " ",
                print colored(str(card.top), card.color),
                print "  |",
            else:
                print "      |",
        print ""

    def _print_bottomrow(self, cards):
        display = []
        print "|",
        for card in cards:
            if card is not None:
                print " ",
                print colored(str(card.bottom), card.color),
                print "  |",
            else:
                print "      |",
        print ""

    def _print_midrow(self, cards, letter_num):
        letter_num = (letter_num * 3) + 97
        display = []
        print "|",
        for card in cards:
            if card is not None:
                print colored(str(card.left), card.color),
                print " ",
                print colored(str(card.right), card.color),
                print "|",
            else:
                print "  " + chr(letter_num) + "   |",
            letter_num = letter_num + 1
        print ""

# --------------- Helper functions ---------------

def load_deck(file='cards.txt'):
    deck = []
    for line in open(file):
        if '#' not in line:
            card_descriptor = [int(x) for x in line.split(',')]
            card_descriptor.append(None)
            deck.append(Card(*card_descriptor))
    return deck

def load_hand(color, deck, size=5):
    hand = []
    for i in range(0, size):
        hand.append(deck.pop(random.randrange(len(deck))))
    for card in hand:
        card.color = color
    return hand

def prompt_location_choice(board):
    flattened = board.flat_list()
    while True:
        selection = raw_input("Place card where? ")
        for spot, letter in zip(board.flat_list(), string.ascii_lowercase):
            if selection == letter:
                location = ord(selection.strip()) - 97
                if flattened[location] is None:
                    return location
        print "Invalid choice, try again."

def prompt_card_choice(hand):
    print "Your hand: "
    for card, letter in zip(hand, string.ascii_lowercase):
        print letter + "."
        card.display()
    while True:
        selection = raw_input("Select your card: ")
        for card, letter in zip(hand, string.ascii_lowercase):
            if letter == selection:
                return card
        print "Invalid choice, try again."

# --------------- Main game loop ---------------

def main():
    """ Core game loop """
    print "WELCOME TO TRIPLE TRIAD"
    deck = load_deck()
    Game(deck).run()
    
main()