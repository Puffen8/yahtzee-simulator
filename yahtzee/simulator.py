from yahtzee.game import Game
from yahtzee.strategy import Strategy
from yahtzee.scorecard import Scorecard

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


from collections import Counter

import os
import json
import csv
from datetime import datetime

from typing import List, Optional


class Simulator:
    def __init__(self, strategy: Strategy, number_of_games: int, trace_history: bool = False) -> None:
        self.strategy = strategy
        self.number_of_games = number_of_games
        self.trace_history = trace_history

        self.game_scorecards: List[Scorecard] = []
        self.scores = np.zeros(self.number_of_games, dtype=int)


    def run(self):
        for i in range(self.number_of_games):
            print(f"Simulating game {i + 1} / {self.number_of_games}", end="\r")
            game = Game(self.strategy)
            game.play_game()
            self.scores[i] = game.scorecard.total_score()
            self.game_scorecards.append(game.scorecard)  # optional if you still want full scorecards

            if self.trace_history:
                print(f"History for game {i + 1}:")
                game.print_history()
                print()

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

    def get_bonus_percentage(self) -> float:
        return sum(1 for sc in self.game_scorecards if sc.has_bonus()) / self.number_of_games * 100 if self.number_of_games > 0 else 0.0
    
    def print_summary(self):
        print(f"Average score over {self.number_of_games} games: {self.average_score()}")
        print(f"Best score: {self.best_score()}")
        print(f"Worst score: {self.worst_score()}")
        print(f"Standard deviation: {self.standard_deviation()}")
        print(f"Median score: {self.median_score()}")
    
    def _calculate_histogram_params(self, values: np.ndarray) -> tuple[int, int, int]:
        """
        Calculate histogram parameters for given score values.

        Args:
            values: Array of score values.

        Returns:
            Tuple (x_min, x_max, num_bins):
                x_min: Minimum score - 5
                x_max: Maximum score + 5
                num_bins: Number of unique scores + 10
        """
        if len(values) == 0:
            return 0, 0, 0

        min_val = int(np.min(values))
        max_val = int(np.max(values))
        x_min = min_val - 5
        x_max = max_val + 5
        num_bins = len(np.unique(values)) + 10

        return x_min, x_max, num_bins


    def plot_upper_section_frequencies(self) -> Optional[plt.Figure]:
        upper_scores = np.array([sc.upper_section_score() for sc in self.game_scorecards])
        if len(upper_scores) == 0:
            return None

        x_min, x_max, num_bins = self._calculate_histogram_params(upper_scores)

        fig = plt.figure(figsize=(10, 6))

        # Get histogram data
        counts, bin_edges = np.histogram(upper_scores, bins=num_bins, range=(x_min, x_max))

        # Color bins differently depending on whether they are below/above 63
        bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
        colors = ['orange' if center < 63 else 'lightgreen' for center in bin_centers]

        plt.bar(bin_centers, counts, width=(bin_edges[1] - bin_edges[0]), 
                color=colors, edgecolor='black')


        plt.title(f"Upper Section Score Distribution over {self.number_of_games} Games")
        plt.xlabel("Upper Section Score")
        plt.ylabel("Frequency")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(range(x_min, x_max + 1, 5))
        ax = plt.gca()
        ax.yaxis.set_major_locator(mticker.MaxNLocator(nbins='auto', integer=True))
        plt.tight_layout()
        return fig



    def plot_score_frequencies(self) -> Optional[plt.Figure]:
        scores = np.array([scorecard.total_score() for scorecard in self.game_scorecards])
        if len(scores) == 0:
            return None

        x_min, x_max, num_bins = self._calculate_histogram_params(scores)

        fig = plt.figure(figsize=(10, 6))
        plt.hist(
            scores,
            bins=num_bins,
            range=(x_min, x_max),
            color='lightgreen',
            edgecolor='black'
        )
        plt.title(f"Score Distribution over {self.number_of_games} Games")
        plt.xlabel("Score")
        plt.ylabel("Frequency")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(range(x_min, x_max + 1, 10))
        ax = plt.gca()
        ax.yaxis.set_major_locator(mticker.MaxNLocator(nbins='auto', integer=True))
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
            "Bonus percentage": self.get_bonus_percentage(),
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
        upper_histogram = self.plot_upper_section_frequencies()
        upper_histogram_file = os.path.join(run_folder, "upper_section_histogram.png")
        if upper_histogram is not None:
            upper_histogram.savefig(upper_histogram_file)
            plt.close(upper_histogram)

        print(f"Results saved in folder: {run_folder}")
