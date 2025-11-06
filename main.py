from yahtzee_simulator.simulator import Simulator
from yahtzee_simulator.strategies.example_strategy import ExampleStrategy


if __name__ == "__main__":
    strategy = ExampleStrategy()
    simulator = Simulator(strategy, 200, trace_history=False)
    simulator.run()
    simulator.print_summary()

