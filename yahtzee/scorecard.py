from enum import Enum, auto
from typing import Dict, List, Optional, Tuple
from yahtzee.score_category import Category, Dice

class Scorecard:
    """Represents a Yahtzee scorecard."""

    def __init__(self) -> None:
        self.scores: Dict[Category, Optional[int]] = {cat: None for cat in Category}

    def __str__(self) -> str:
        lines = []
        for category in Category:
            score = self.scores[category]
            score_str = str(score) if score is not None else "-"
            lines.append(f"{category.code:<20} {score_str}")
        lines.append("-" * 22)
        lines.append(f"{'Upper Section Total':<20} {self.upper_section_score()}")
        lines.append(f"{'Upper Section Bonus':<20} {'50' if self.upper_section_score() >= 63 else '0'}")
        lines.append(f"{'Total Score':<20} {self.total_score()}\n\n")
        return "\n".join(lines)

    def is_complete(self) -> bool:
        """Return True if all categories are filled."""
        return all(v is not None for v in self.scores.values())

    def available_categories(self) -> List[Category]:
        """Return a list of unfilled categories."""
        return [cat for cat, val in self.scores.items() if val is None]

    def total_score(self) -> int:
        """Return the total score including upper section bonus."""
        base = sum(v or 0 for v in self.scores.values())
        if self.upper_section_score() >= 63:
            base += 50
        return base
    
    def has_bonus(self) -> bool:
        """Return True if the upper section bonus has been achieved."""
        return self.upper_section_score() >= 63
    
    def upper_categories(self) -> list[Category]:
        return [
            Category.ONES,
            Category.TWOS,
            Category.THREES,
            Category.FOURS,
            Category.FIVES,
            Category.SIXES,
        ]
    
    def is_upper_section(self, cat: Category) -> bool:
        return cat in self.upper_categories()

    def upper_section_score(self) -> int:
        """Return the subtotal for the upper section (ones–sixes)."""
        return sum(self.scores[c] or 0 for c in self.upper_categories())

    def score_for_category(self, dice: Dice, category: Category) -> int:
        """Return the points this roll would score in the given category."""
        counts = {i: dice.count(i) for i in range(1, 7)}
        # Return the maximum possible score for the category
        if category == Category.ONES:
            return counts[1] * 1
        if category == Category.TWOS:
            return counts[2] * 2
        if category == Category.THREES:
            return counts[3] * 3
        if category == Category.FOURS:
            return counts[4] * 4
        if category == Category.FIVES:
            return counts[5] * 5
        if category == Category.SIXES:
            return counts[6] * 6
        if category == Category.PAIR:
            pairs = [val for val, count in counts.items() if count >= 2]
            return max(pairs) * 2 if pairs else 0
        if category == Category.TWO_PAIR:
            pairs = [val for val, count in counts.items() if count >= 2]
            if len(pairs) >= 2:
                top_two = sorted(pairs, reverse=True)[:2]
                return sum(val * 2 for val in top_two)
            return 0
        if category == Category.THREE_OF_KIND:
            triples = [val for val, cnt in counts.items() if cnt >= 3]
            return max(triples) * 3 if triples else 0
        if category == Category.FOUR_OF_KIND:
            quads = [val for val, cnt in counts.items() if cnt >= 4]
            return max(quads) * 4 if quads else 0
        if category == Category.SMALL_STRAIGHT:
            return 15 if set(dice) == {1, 2, 3, 4, 5} else 0
        if category == Category.LARGE_STRAIGHT:
            return 20 if set(dice) == {2, 3, 4, 5, 6} else 0
        if category == Category.FULL_HOUSE:
            return sum(dice) if sorted(counts.values(), reverse=True)[:2] in ([3, 2], [2, 3]) else 0
        if category == Category.YAHTZEE:
            return 50 if any(v == 5 for v in counts.values()) else 0
        if category == Category.CHANCE:
            return sum(dice)

        raise ValueError(f"Unknown category: {category}")

    def set_score(self, dice: Dice, category: Category) -> None:
        """Fill a category with the score from this roll."""
        if self.scores[category] is not None:
            raise ValueError(f"Category {category} already filled.")
        self.scores[category] = self.score_for_category(dice, category)

    def get_available_categories_with_scores(self, dice: Dice) -> Dict[Category, int]:
        """Return a dictionary of available categories that give a nonzero score."""
        return {
            cat: score
            for cat in self.available_categories()
            if (score := self.score_for_category(dice, cat)) > 0
        }
    
    def print_scorecard(self):
        """Print the current state of the scorecard."""
        for category in Category:
            score = self.scores[category]
            score_str = str(score) if score is not None else "-"
            print(f"{category.name.replace('_', ' ').title():<20} {score_str}")
        print("-" * 22)
        print(f"{'Upper Section Total':<20} {self.upper_section_score()}")
        print(f"{'Upper Section Bonus':<20} {'50' if self.upper_section_score() >= 63 else '0'}")
        print()
        print(f"{'Total Score':<20} {self.total_score()}")
        print()
        print('' * 40)