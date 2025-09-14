from typing import Dict, List
from yahtzee.score_category import Category


def get_least_worth_category_left(categories: List[Category]) -> Category:
    """Return the category with the lowest possible max score from the possible categories."""
    return min(categories, key=lambda cat: cat.max_score)