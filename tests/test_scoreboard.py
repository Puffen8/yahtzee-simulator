import unittest
from yahtzee.scorecard import Scorecard
from yahtzee.score_category import Category

class TestScorecard(unittest.TestCase):
    def setUp(self):
        """Create a new Scorecard before each test."""
        self.scorecard = Scorecard()

    def test_no_scores(self):
        dice = (0, 0, 0, 0, 0)

        for category in Category:
            score = self.scorecard.score_for_category(dice, category)
            self.assertEqual(score, 0)

    def test_upper_section_scoring(self):
        dice = (1, 1, 1, 2, 3)
        score = self.scorecard.score_for_category(dice, Category.ONES)
        self.assertEqual(score, 3)

        score = self.scorecard.score_for_category(dice, Category.TWOS)
        self.assertEqual(score, 2)

        score = self.scorecard.score_for_category(dice, Category.THREES)
        self.assertEqual(score, 3)

        score = self.scorecard.score_for_category(dice, Category.FOURS)
        self.assertEqual(score, 0)

        score = self.scorecard.score_for_category(dice, Category.SIXES)
        self.assertEqual(score, 0)

    def test_pair(self):
        dice = (3, 3, 4, 5, 6)
        score = self.scorecard.score_for_category(dice, Category.PAIR)
        self.assertEqual(score, 6)

    def test_pair_2(self):
        dice = (3, 3, 4, 6, 6)
        score = self.scorecard.score_for_category(dice, Category.PAIR)
        self.assertEqual(score, 12)

    def test_two_pair(self):
        dice = (3, 3, 4, 4, 6)
        score = self.scorecard.score_for_category(dice, Category.TWO_PAIR)
        self.assertEqual(score, 14)

    def test_three_of_a_kind(self):
        dice = (2, 2, 2, 5, 6)
        score = self.scorecard.score_for_category(dice, Category.THREE_OF_KIND)
        self.assertEqual(score, 6)

    def test_four_of_a_kind(self):
        dice = (5, 5, 5, 5, 6)
        score = self.scorecard.score_for_category(dice, Category.FOUR_OF_KIND)
        self.assertEqual(score, 20)

    def test_small_straight(self):
        dice = (1, 2, 3, 4, 5)
        score = self.scorecard.score_for_category(dice, Category.SMALL_STRAIGHT)
        self.assertEqual(score, 15)

    def test_large_straight(self):
        dice = (2, 3, 4, 5, 6)
        score = self.scorecard.score_for_category(dice, Category.LARGE_STRAIGHT)
        self.assertEqual(score, 20)

    def test_full_house(self):
        dice = (3, 3, 3, 5, 5)
        score = self.scorecard.score_for_category(dice, Category.FULL_HOUSE)
        self.assertEqual(score, 19)

    def test_chance(self):
        dice = (1, 2, 3, 5, 6)
        score = self.scorecard.score_for_category(dice, Category.CHANCE)
        self.assertEqual(score, 17)

    def test_yahtzee(self):
        dice = (6, 6, 6, 6, 6)
        score = self.scorecard.score_for_category(dice, Category.YAHTZEE)
        self.assertEqual(score, 50)




if __name__ == "__main__":
    unittest.main()
    # python -m unittest discover -s tests
