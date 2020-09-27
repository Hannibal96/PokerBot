from enum import Enum


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Suits(Enum):
    Heart = 0
    Diamond = 1
    Spade = 2
    Club = 3


class Number(Enum):
    Ace = 14
    Duce = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13


class Card:
    def __init__(self, number, suit):
        if number not in Number:
            assert False
        if suit not in Suits:
            assert False
        self.number = number
        self.suit = suit

    def __eq__(self, other):
        return self.number.value == other.number.value and self.suit.value == other.suit.value

    def __lt__(self, other):
        if self.number.value == other.number.value:
            return self.suit.value < other.suit.value
        return self.number.value < other.number.value

    def __str__(self):
        suits_symbols = [Color.RED+'♥'+Color.END, Color.YELLOW+'♦'+Color.END, Color.PURPLE+'♠'+Color.END, Color.GREEN+'♣'+Color.END]
        numbers_symbols = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return '|'+numbers_symbols[self.number.value-2]+suits_symbols[self.suit.value]+'|'


