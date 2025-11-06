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
        self.history = []  # To trace the history of the game

    def roll_dice(self, number_of_dice: int) -> tuple[int, ...]:
        self.rolls_left -= 1
        return tuple(randint(1, 6) for _ in range(number_of_dice))
    
    def play_turn(self) -> None:
        self.rolls_left = 3
        turn_history = []
        dice = self.roll_dice(5)
        while self.rolls_left > 0:
            turn_history.append(f"Roll number {3 - self.rolls_left}: {dice}")
            if self.strategy.should_finish_turn(dice, self.rolls_left, self.scorecard):
                category = self.strategy.choose_category(dice, self.scorecard)
                turn_history.append(f"Finishing turn, choosing category: {category}")
                self.scorecard.set_score(dice, category)
                return
            dice_to_keep = self.strategy.choose_dice_to_keep(dice, self.rolls_left, self.scorecard)
            turn_history.append(f"Continuing turn, keeping dice: {dice_to_keep}")
            dice = dice_to_keep + self.roll_dice(5 - len(dice_to_keep))
        # Must finish turn since no rolls left
        turn_history.append(f"Roll number {3 - self.rolls_left}: {dice}")
        category = self.strategy.choose_category(dice, self.scorecard)
        turn_history.append(f"No rolls left, choosing category: {category}")
        self.scorecard.set_score(dice, category)
        turn_history.append(f"Current scorecard:\n {self.scorecard}")
        self.history.append(turn_history)

    def play_game(self) -> Scorecard:
        for turn in Category:
            self.play_turn()
    
    def print_history(self) -> None:
        for turn_number, turn in enumerate(self.history, start=1):
            print(f"Turn {turn_number}:")
            for decision in turn:
                print(f"  {decision}")
        print(f"Final Scorecard:\n{self.scorecard}")
