from yahtzee.strategy import Strategy
from yahtzee.score_category import Category, Dice
from yahtzee.scorecard import Scorecard
from yahtzee.strategy_helpers import get_least_worth_category_left

class TestStrategy(Strategy):
    """Example strategy: always stop if a high-value category is possible."""
    def should_finish_turn(self, dice: Dice, rolls_left: int, scorecard: Scorecard) -> bool:
        return rolls_left == 3 # Always finish after first roll

    def choose_dice_to_keep(self, dice: Dice, rolls_left: int, scorecard: Scorecard) -> tuple[int]:
        dice_to_keep = tuple()
        return dice

    def choose_category(self, dice: Dice, scorecard: Scorecard) -> Category:
        possible = scorecard.get_available_categories_with_scores(dice)
        if possible:
            return max(possible, key=possible.get)
        else:
            return get_least_worth_category_left(scorecard.available_categories())