from yahtzee.game import Game
from yahtzee.strategy import Strategy

class Simulator:
    def __init__(self, strategy: Strategy, number_of_games: int) -> None:
        self.strategy = strategy
        self.number_of_games = number_of_games
        self.game_scorecards = []

    def run(self):
        for _ in range(self.number_of_games):
            game = Game(self.strategy)
            scorecard = game.play_game()
            self.game_scorecards.append(scorecard)
            
        print("All game scores:")
        for scorecard in self.game_scorecards:
            scorecard.print_scorecard()
            # print(f"Game score: {score}")