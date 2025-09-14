from yahtzee.simulator import Simulator
from yahtzee.strategies.test_strategy import TestStrategy



if __name__ == "__main__":
    strategy = TestStrategy()
    simulator = Simulator(strategy, 100)
    simulator.run()