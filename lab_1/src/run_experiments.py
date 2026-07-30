import argparse
import csv
import os
import random
import sys
import time

sys.setrecursionlimit(1000000)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from algorithms import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    heap_sort,
)

ALGORITHMS = {
    "BubbleSort": lambda arr, **kw: bubble_sort(arr),
    "SelectionSort": lambda arr, **kw: selection_sort(arr),
    "InsertionSort": lambda arr, **kw: insertion_sort(arr),
    "MergeSort": lambda arr, **kw: merge_sort(arr),
    "QuickSort": lambda arr, **kw: quick_sort(arr, 0, len(arr) - 1),
    "HeapSort": lambda arr, **kw: heap_sort(arr),
}

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")


def parse_args():
    p = argparse.ArgumentParser(description="Sorting algorithm timing experiments")
    p.add_argument("--sizes", default="1000,5000,10000,20000,50000,100000",
                    help="Comma-separated input sizes (default: 1000,5000,10000,20000,50000,100000)")
    p.add_argument("--trials", type=int, default=5,
                    help="Number of trials per (algorithm, size, case) (default: 5)")
    p.add_argument("--seed", type=int, default=42,
                    help="Random seed (default: 42)")
    p.add_argument("--timeout", type=float, default=60.0,
                    help="Timeout in seconds per trial (default: 60.0)")
    p.add_argument("--cases", default="Best,Average,Worst",
                    help="Comma-separated cases: Best,Average,Worst (default: all)")
    return p.parse_args()


def generate_case(case, size):
    if case == "Best":
        return list(range(size))
    elif case == "Worst":
        return list(range(size, 0, -1))
    else:
        arr = list(range(size))
        random.shuffle(arr)
        return arr


def run_trial(alg_func, arr):
    started = time.perf_counter()
    alg_func(arr)
    return time.perf_counter() - started


def main():
    args = parse_args()
    sizes = [int(s.strip()) for s in args.sizes.split(",")]
    trials = args.trials
    cases = [c.strip() for c in args.cases.split(",")]
    timeout = args.timeout
    random.seed(args.seed)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    csv_path = os.path.join(RESULTS_DIR, "sorting_results.csv")
    skipped = set()

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Algorithm", "Case", "Size", "Trial", "Time_sec"])

        for size in sizes:
            for case_name in cases:
                for alg_name, alg_func in ALGORITHMS.items():
                    if (alg_name, case_name) in skipped:
                        for trial in range(1, trials + 1):
                            writer.writerow([alg_name, case_name, size, trial, "skipped"])
                        sys.stdout.write(f"{alg_name:15s} {case_name:8s} n={size:6d} trials=1-{trials} skipped\n")
                        sys.stdout.flush()
                        continue

                    timed_out = False
                    for trial in range(1, trials + 1):
                        if timed_out:
                            writer.writerow([alg_name, case_name, size, trial, "skipped"])
                            continue

                        arr = generate_case(case_name, size)
                        elapsed = run_trial(alg_func, arr)
                        writer.writerow([alg_name, case_name, size, trial, f"{elapsed:.6f}"])
                        sys.stdout.write(f"{alg_name:15s} {case_name:8s} n={size:6d} trial={trial}/{trials} time={elapsed:.4f}s\n")
                        sys.stdout.flush()

                        if elapsed > timeout:
                            timed_out = True
                            skipped.add((alg_name, case_name))

    print(f"\nResults written to {csv_path}")


if __name__ == "__main__":
    main()
