import argparse
import csv
import os
import random
import sys
import time

sys.setrecursionlimit(1000000)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from algorithms import (
    activity_brute_force,
    activity_greedy_iterative,
    knapsack_brute_force,
    knapsack_greedy_ratio,
)

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")


def parse_args():
    p = argparse.ArgumentParser(description="Activity Selection and 0/1 Knapsack experiments")
    p.add_argument("--as-sizes", default="5,6,7,8,9,10,11,12,13,14,15,16,18,20,22",
                    help="Activity selection input sizes (default: 5-22 step 1-2)")
    p.add_argument("--kp-sizes", default="5,6,7,8,9,10,11,12,13,14,15,16,18,20,22",
                    help="Knapsack input sizes (default: 5-22 step 1-2)")
    p.add_argument("--as-trials", type=int, default=10,
                    help="Trials per (AS algorithm, size) (default: 10)")
    p.add_argument("--kp-trials", type=int, default=5,
                    help="Trials per (KP algorithm, size) (default: 5)")
    p.add_argument("--seed", type=int, default=42,
                    help="Random seed (default: 42)")
    p.add_argument("--timeout", type=float, default=30.0,
                    help="Timeout in seconds per trial (default: 30.0)")
    return p.parse_args()


def generate_activity_set(n):
    activities = []
    for _ in range(n):
        start = random.randint(0, 999)
        duration = random.randint(11, 100)
        finish = start + duration
        activities.append((start, finish))
    return activities


def generate_knapsack_instance(n):
    values = [random.randint(1, 100) for _ in range(n)]
    weights = [random.randint(1, 50) for _ in range(n)]
    capacity = int(0.4 * sum(weights))
    return values, weights, capacity


def _time_call(func, *args):
    t0 = time.perf_counter()
    func(*args)
    return time.perf_counter() - t0


def run_activity_experiments(as_sizes, trials, timeout):
    bf_skipped = False
    csv_path = os.path.join(RESULTS_DIR, "activity_results.csv")
    quality_path = os.path.join(RESULTS_DIR, "activity_quality.csv")

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Algorithm", "Size", "Trial", "Time_sec"])

        for size in as_sizes:
            for trial in range(1, trials + 1):
                acts = generate_activity_set(size)
                elapsed_g = _time_call(activity_greedy_iterative, acts)
                writer.writerow(["GreedyIterative", size, trial, f"{elapsed_g:.10f}"])

                if bf_skipped:
                    writer.writerow(["BruteForce", size, trial, "skipped"])
                else:
                    elapsed_bf = _time_call(activity_brute_force, acts)
                    writer.writerow(["BruteForce", size, trial, f"{elapsed_bf:.10f}"])
                    if elapsed_bf > timeout:
                        bf_skipped = True
                    sys.stdout.write(f"AS n={size:2d} trial={trial}/{trials} BF={elapsed_bf:.6f}s G={elapsed_g:.6f}s\n")
                    sys.stdout.flush()

    bf_skipped = False
    with open(quality_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Size", "Trial", "GreedyCount", "OptimalCount", "QualityPct"])
        for size in as_sizes:
            for trial in range(1, trials + 1):
                acts = generate_activity_set(size)
                greedy_count = activity_greedy_iterative(acts)
                if bf_skipped:
                    writer.writerow([size, trial, greedy_count, "", ""])
                else:
                    t0 = time.perf_counter()
                    optimal = activity_brute_force(acts)
                    elapsed_bf = time.perf_counter() - t0
                    quality = (greedy_count / optimal) * 100.0
                    writer.writerow([size, trial, greedy_count, optimal, f"{quality:.2f}"])
                    if elapsed_bf > timeout:
                        bf_skipped = True

    print(f"  Activity results  -> {csv_path}")
    print(f"  Activity quality  -> {quality_path}")


def run_knapsack_experiments(kp_sizes, trials, timeout):
    bf_skipped = False
    csv_path = os.path.join(RESULTS_DIR, "knapsack_results.csv")
    quality_path = os.path.join(RESULTS_DIR, "knapsack_quality.csv")

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Algorithm", "Size", "Trial", "Time_sec"])

        for size in kp_sizes:
            for trial in range(1, trials + 1):
                values, weights, capacity = generate_knapsack_instance(size)
                elapsed_g = _time_call(knapsack_greedy_ratio, values, weights, capacity)
                writer.writerow(["GreedyRatio", size, trial, f"{elapsed_g:.10f}"])

                if bf_skipped:
                    writer.writerow(["BruteForce", size, trial, "skipped"])
                else:
                    elapsed_bf = _time_call(knapsack_brute_force, values, weights, capacity)
                    writer.writerow(["BruteForce", size, trial, f"{elapsed_bf:.10f}"])
                    if elapsed_bf > timeout:
                        bf_skipped = True
                    sys.stdout.write(f"KP n={size:2d} trial={trial}/{trials} BF={elapsed_bf:.6f}s G={elapsed_g:.6f}s\n")
                    sys.stdout.flush()

    bf_skipped = False
    with open(quality_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Size", "Trial", "GreedyValue", "OptimalValue", "QualityPct"])
        for size in kp_sizes:
            for trial in range(1, trials + 1):
                values, weights, capacity = generate_knapsack_instance(size)
                greedy_val, _, _ = knapsack_greedy_ratio(values, weights, capacity)
                if bf_skipped:
                    writer.writerow([size, trial, greedy_val, "", ""])
                else:
                    t0 = time.perf_counter()
                    optimal = knapsack_brute_force(values, weights, capacity)
                    elapsed_bf = time.perf_counter() - t0
                    quality = (greedy_val / optimal) * 100.0
                    writer.writerow([size, trial, greedy_val, optimal, f"{quality:.2f}"])
                    if elapsed_bf > timeout:
                        bf_skipped = True

    print(f"  Knapsack results  -> {csv_path}")
    print(f"  Knapsack quality  -> {quality_path}")


def main():
    args = parse_args()
    random.seed(args.seed)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    as_sizes = [int(s.strip()) for s in args.as_sizes.split(",")]
    kp_sizes = [int(s.strip()) for s in args.kp_sizes.split(",")]

    print("Running Activity Selection experiments...")
    run_activity_experiments(as_sizes, args.as_trials, args.timeout)
    print("Running 0/1 Knapsack experiments...")
    run_knapsack_experiments(kp_sizes, args.kp_trials, args.timeout)
    print(f"\nAll results written to {RESULTS_DIR}/")


if __name__ == "__main__":
    main()
