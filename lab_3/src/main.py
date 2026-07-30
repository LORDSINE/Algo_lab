import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from run_experiments import main as run_experiments_main
from plot_results import main as plot_results_main


def main():
    print("Running lab 3 experiments...")
    run_experiments_main()
    print("Generating lab 3 figures...")
    plot_results_main()
    print("Lab 3 complete.")


if __name__ == "__main__":
    main()
