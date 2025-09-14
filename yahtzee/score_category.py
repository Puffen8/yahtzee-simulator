from enum import Enum

class Category(Enum):
    """Yahtzee score categories with max and min non-zero scores."""
    
    ONES = ("ones", 5, 1)
    TWOS = ("twos", 10, 2)
    THREES = ("threes", 15, 3)
    FOURS = ("fours", 20, 4)
    FIVES = ("fives", 25, 5)
    SIXES = ("sixes", 30, 6)
    PAIR = ("pair", 12, 2)  # max pair is 6+6, min nonzero is 1+1
    TWO_PAIR = ("two_pair", 22, 6)  # e.g., 6+6 + 5+5 max, min nonzero 1+1 + 2+2
    THREE_OF_KIND = ("three_kind", 18, 3)  # max 6*3=18
    FOUR_OF_KIND = ("four_kind", 24, 4)    # max 6*4=24
    FULL_HOUSE = ("full_house", 28, 7)     # max 6+6+6 + 5+5 etc.
    SMALL_STRAIGHT = ("small_straight", 15, 15)  # fixed
    LARGE_STRAIGHT = ("large_straight", 20, 20)  # fixed
    CHANCE = ("chance", 30, 5)            # max sum 30 (5*6), min nonzero 1
    YAHTZEE = ("yahtzee", 50, 50)          # max fixed, min nonzero 1*5

    def __init__(self, code, max_score, min_nonzero):
        self._code = code
        self.max_score = max_score
        self.min_nonzero = min_nonzero

Dice = tuple[int, int, int, int, int]  # A roll of five dice