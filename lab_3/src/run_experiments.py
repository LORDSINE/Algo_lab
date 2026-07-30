import argparse
import csv
import os
import random
import signal
import sys
import time

sys.setrecursionlimit(1000000)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from algorithms import fib_recursive, fib_memoized, tsp_brute_force, tsp_held_karp

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")


class TimeoutError(Exception):
    pass


def _timeout_handler(signum, frame):
    raise TimeoutError


signal.signal(signal.SIGALRM, _timeout_handler)


def run_with_timeout(func, args, timeout_sec):
    signal.alarm(int(timeout_sec))
    try:
        start = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - start
        signal.alarm(0)
        return result, elapsed
    except TimeoutError:
        signal.alarm(0)
        return None, None


def generate_symmetric_dist_matrix(n, seed):
    rng = random.Random(seed)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = rng.randint(1, 100)
            matrix[i][j] = d
            matrix[j][i] = d
    return matrix


def parse_args():
    p = argparse.ArgumentParser(description="Fibonacci and TSP experiments")
    p.add_argument("--fib-sizes", default="5,10,15,20,25,30,35",
                    help="Fibonacci input sizes (default: 5,10,15,20,25,30,35)")
    p.add_argument("--tsp-sizes", default="4,5,6,7,8,9,10,11,12",
                    help="TSP input sizes (default: 4,5,6,7,8,9,10,11,12)")
    p.add_argument("--trials", type=int, default=3,
                    help="Trials per (algorithm, size) (default: 3)")
    p.add_argument("--seed", type=int, default=42,
                    help="Random seed (default: 42)")
    p.add_argument("--fib-timeout", type=float, default=30.0,
                    help="Timeout in seconds for Fibonacci (default: 30.0)")
    p.add_argument("--tsp-timeout", type=float, default=60.0,
                    help="Timeout in seconds for TSP (default: 60.0)")
    return p.parse_args()


def run_fib_experiments(fib_sizes, trials, seed, timeout):
    random.seed(seed)
    csv_path = os.path.join(RESULTS_DIR, "fib_results.csv")

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Algorithm", "Size", "Trial", "Time_sec"])
        for algo_name, algo_func in [
            ("FibRecursive", fib_recursive),
            ("FibMemoized", fib_memoized),
        ]:
            for n in fib_sizes:
                for t in range(trials):
                    result, elapsed = run_with_timeout(algo_func, (n,), timeout)
                    if result is None:
                        print(f"Skip {algo_name} n={n}: >{timeout}s")
                        break
                    writer.writerow([algo_name, n, t + 1, f"{elapsed:.10f}"])
                    print(f"{algo_name:14s} n={n:2d} trial={t+1}/{trials} time={elapsed:.6f}s")

    print(f"  Fibonacci results -> {csv_path}")


def run_tsp_experiments(tsp_sizes, trials, seed, timeout):
    csv_path = os.path.join(RESULTS_DIR, "tsp_results.csv")

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Algorithm", "Size", "Trial", "Time_sec"])
        for n in tsp_sizes:
            for t in range(trials):
                s = seed + t * 100 + n
                dist = generate_symmetric_dist_matrix(n, s)
                for algo_name, algo_func in [
                    ("TSPBruteForce", tsp_brute_force),
                    ("TSPHeldKarp", tsp_held_karp),
                ]:
                    result, elapsed = run_with_timeout(algo_func, (dist,), timeout)
                    if result is None:
                        print(f"Skip {algo_name} n={n}: >{timeout}s")
                        break
                    writer.writerow([algo_name, n, t + 1, f"{elapsed:.10f}"])
                    print(f"{algo_name:14s} n={n:2d} trial={t+1}/{trials} time={elapsed:.6f}s")

    print(f"  TSP results        -> {csv_path}")


def main():
    args = parse_args()
    os.makedirs(RESULTS_DIR, exist_ok=True)

    fib_sizes = [int(s.strip()) for s in args.fib_sizes.split(",")]
    tsp_sizes = [int(s.strip()) for s in args.tsp_sizes.split(",")]

    print("Running Fibonacci experiments...")
    run_fib_experiments(fib_sizes, args.trials, args.seed, args.fib_timeout)
    print("Running TSP experiments...")
    run_tsp_experiments(tsp_sizes, args.trials, args.seed, args.tsp_timeout)
    print(f"\nAll results written to {RESULTS_DIR}/")


if __name__ == "__main__":
    main()
