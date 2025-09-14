from enum import Enum

class Category(Enum):
    """Yahtzee score categories with max and min non-zero scores."""
    
    ONES = ("Ones", 5, 1)
    TWOS = ("Twos", 10, 2)
    THREES = ("Threes", 15, 3)
    FOURS = ("Fours", 20, 4)
    FIVES = ("Fives", 25, 5)
    SIXES = ("Sixes", 30, 6)
    PAIR = ("Pair", 12, 2)  # max pair is 6+6, min nonzero is 1+1
    TWO_PAIR = ("Two Pair", 22, 6)  # e.g., 6+6 + 5+5 max, min nonzero 1+1 + 2+2
    THREE_OF_KIND = ("Three of a Kind", 18, 3)  # max 6*3=18
    FOUR_OF_KIND = ("Four of a Kind", 24, 4)    # max 6*4=24
    FULL_HOUSE = ("Full House", 28, 7)     # max 6+6+6 + 5+5 etc.
    SMALL_STRAIGHT = ("Small Straight", 15, 15)  # fixed
    LARGE_STRAIGHT = ("Large Straight", 20, 20)  # fixed
    CHANCE = ("Chance", 30, 5)            # max sum 30 (5*6), min nonzero 1
    YAHTZEE = ("Yahtzee", 50, 50)          # max fixed, min nonzero 1*5

    def __init__(self, code, max_score, min_nonzero):
        self.code = code
        self.max_score = max_score
        self.min_nonzero = min_nonzero

Dice = tuple[int, int, int, int, int]  # A roll of five dice