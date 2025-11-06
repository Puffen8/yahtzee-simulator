from dataclasses import dataclass
from enum import Enum, auto
from yahtzee.score_category import Category, Dice


class DecisionType(Enum):
    FINISH_TURN = auto()
    KEEP_DICE = auto()
    CHOOSE_CATEGORY = auto()


@dataclass
class Decision:
    type: DecisionType
    description: str
