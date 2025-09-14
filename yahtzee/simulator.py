from yahtzee.game import Game
from yahtzee.strategy import Strategy
from yahtzee.scorecard import Scorecard

import numpy as np
import matplotlib.pyplot as plt

from collections import Counter

import os
import json
import csv
from datetime import datetime

from typing import List, Optional


class Simulator:
    def __init__(self, strategy: Strategy, number_of_games: int) -> None:
        self.strategy = strategy
        self.number_of_games = number_of_games
        self.game_scorecards: List[Scorecard] = []
        self.scores = np.zeros(self.number_of_games, dtype=int)


    def run(self):
        for i in range(self.number_of_games):
            game = Game(self.strategy)
            scorecard = game.play_game()
            self.scores[i] = scorecard.total_score()
            self.game_scorecards.append(scorecard)  # optional if you still want full scorecards

        self.save_results()

    
    def average_score(self) -> float:
        return float(np.mean(self.scores)) if self.number_of_games > 0 else 0.0

    def median_score(self) -> float:
        return float(np.median(self.scores)) if self.number_of_games > 0 else 0.0

    def best_score(self) -> int:
        return int(np.max(self.scores)) if self.number_of_games > 0 else 0

    def worst_score(self) -> int:
        return int(np.min(self.scores)) if self.number_of_games > 0 else 0

    def standard_deviation(self) -> float:
        return float(np.std(self.scores)) if self.number_of_games > 0 else 0.0


    
    def print_summary(self):
        print(f"Average score over {self.number_of_games} games: {self.average_score()}")
        print(f"Best score: {self.best_score()}")
        print(f"Worst score: {self.worst_score()}")
        print(f"Standard deviation: {self.standard_deviation()}")
        print(f"Median score: {self.median_score()}")


    def plot_score_frequencies(self, bins: int = 100) -> plt.Figure:
        """
        Plot a histogram of game scores showing the frequency distribution.

        Args:
            bins: Number of bins to divide the scores into.
        """

        # Convert scores to a NumPy array if not already
        scores = np.array([scorecard.total_score() for scorecard in self.game_scorecards])

        fig = plt.figure(figsize=(10, 6))
        plt.hist(scores, bins=bins, color='skyblue', edgecolor='black')
        plt.title(f"Score Distribution over {self.number_of_games} Games")
        plt.xlabel("Score")
        plt.ylabel("Frequency")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        return fig    



    def save_results(self):
        # Get strategy name
        strategy_name = self.strategy.__class__.__name__

        # Base folder for results
        base_folder = "results"
        strategy_folder = os.path.join(base_folder, strategy_name)

        # Create folder if it doesn't exist
        os.makedirs(strategy_folder, exist_ok=True)

        # Create a new subfolder for this run
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        run_folder = os.path.join(strategy_folder, f"run_{timestamp}")
        os.makedirs(run_folder, exist_ok=True)

        # Save raw scores
        scores_file = os.path.join(run_folder, "scores.txt")
        with open(scores_file, "w") as f:
            for scorecard in self.game_scorecards:
                f.write(f"{scorecard}")

        # Save summary + metadata
        summary = {
            "average": self.average_score(),
            "median": self.median_score(),
            "best": self.best_score(),
            "worst": self.worst_score(),
            "std_dev": self.standard_deviation(),
            "Bonus percentage": sum(1 for sc in self.game_scorecards if sc.has_bonus()) / self.number_of_games * 100 if self.number_of_games > 0 else 0.0,
            "number_of_games": self.number_of_games,
            "time": timestamp
        }
        summary_file = os.path.join(run_folder, "summary.json")
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=4)

        # Save histogram plot
        histogram = self.plot_score_frequencies()
        histogram_file = os.path.join(run_folder, "histogram.png")
        if histogram is not None:
            histogram.savefig(histogram_file)
            plt.close(histogram)

        # Plot Upper section score frequencies

        print(f"Results saved in folder: {run_folder}")
