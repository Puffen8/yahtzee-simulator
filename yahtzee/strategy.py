from abc import ABC, abstractmethod
from typing import List
from yahtzee.score_category import Category, Dice
from yahtzee.scorecard import Scorecard

class Strategy(ABC):
    """Abstract base class for Yahtzee strategies."""

    @abstractmethod
    def should_finish_turn(self, dice: Dice, rolls_left: int, scorecard: Scorecard) -> bool:
        """
        Decide whether to stop rolling and score this turn.
        """

    @abstractmethod
    def choose_dice_to_keep(self, dice: Dice, rolls_left: int, scorecard: Scorecard) -> tuple[int]:
        """
        Decide which dice indices to keep if rolling again.
        """

    @abstractmethod
    def choose_category(self, dice: Dice, scorecard: Scorecard) -> Category:
        """
        Decide which category to fill if stopping.
        """
