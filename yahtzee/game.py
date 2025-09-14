from yahtzee.scorecard import Scorecard
from yahtzee.score_category import Category
from random import randint
from yahtzee.score_category import Dice
from yahtzee.strategy import Strategy



class Game:
    def __init__(self, strategy: Strategy) -> None:
        self.scorecard = Scorecard()
        self.strategy = strategy
        self.rolls_left = 3

    def roll_dice(self, number_of_dice: int) -> tuple[int, ...]:
        self.rolls_left -= 1
        return tuple(randint(1, 6) for _ in range(number_of_dice))
    
    def play_turn(self) -> None:
        self.rolls_left = 3
        dice = self.roll_dice(5)
        while self.rolls_left > 0:
            if self.strategy.should_finish_turn(dice, self.rolls_left, self.scorecard):
                category = self.strategy.choose_category(dice, self.scorecard)
                self.scorecard.set_score(dice, category)
                return
            dice_to_keep = self.strategy.choose_dice_to_keep(dice, self.rolls_left, self.scorecard)
            dice = dice_to_keep + self.roll_dice(5 - len(dice_to_keep))
        # Must finish turn since no rolls left
        category = self.strategy.choose_category(dice, self.scorecard)
        self.scorecard.set_score(dice, category)

    def play_game(self) -> Scorecard:
        for turn in Category:
            self.play_turn()
        return self.scorecard