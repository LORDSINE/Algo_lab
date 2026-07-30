import csv
import os
import statistics

import matplotlib.pyplot as plt

try:
    plt.style.use("seaborn-v0_8")
except Exception:
    pass

plt.rcParams.update({
    'font.size': 13,
    'axes.titlesize': 15,
    'axes.labelsize': 14,
    'legend.fontsize': 11,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'lines.linewidth': 2.5,
    'lines.markersize': 8,
})

RESULTS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "results"
)
FIGURES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "figures_3"
)
os.makedirs(FIGURES_DIR, exist_ok=True)

STUDENT = "Prajwal Ghimire (22)"


def read_csv(path):
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["Size"] = int(row["Size"])
            row["Trial"] = int(row["Trial"])
            row["Time_sec"] = float(row["Time_sec"])
            rows.append(row)
    return rows


def plot_fib_full_range(fib_rows):
    fig, ax = plt.subplots(figsize=(14, 8))
    colors = {"FibRecursive": "#1f77b4", "FibMemoized": "#ff7f0e"}
    markers = {"FibRecursive": "o", "FibMemoized": "s"}
    for algo, label in [
        ("FibRecursive", "FibRecursive O(2\u207f)"),
        ("FibMemoized", "FibMemoized O(n)"),
    ]:
        pts = [(r["Size"], r["Time_sec"]) for r in fib_rows if r["Algorithm"] == algo]
        if pts:
            xs, ys = zip(*sorted(pts))
            ax.plot(xs, ys, marker=markers[algo], color=colors[algo],
                    markersize=10, label=label, linewidth=3)
    ax.set_xlabel("n (input size)")
    ax.set_ylabel("Time (sec)")
    ax.set_title(f"Fibonacci Runtime Comparison - {STUDENT}", fontsize=16, fontweight="bold")
    ax.legend(loc="upper left", framealpha=0.9)
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "fib_full_range.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_fib_recursive_log(fib_rows):
    fig, ax = plt.subplots(figsize=(14, 8))
    pts = [(r["Size"], r["Time_sec"]) for r in fib_rows if r["Algorithm"] == "FibRecursive"]
    if pts:
        xs, ys = zip(*sorted(pts))
        ax.plot(xs, ys, "o-", color="#1f77b4", markersize=10, linewidth=3, label="FibRecursive")
    ax.set_xlabel("n (input size)")
    ax.set_ylabel("Time (sec)")
    ax.set_title(f"Recursive Fibonacci (log scale) - {STUDENT}", fontsize=16, fontweight="bold")
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3, which="both")
    ax.legend(loc="upper left", framealpha=0.9)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "fib_recursive_log.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_fib_memoized_linear(fib_rows):
    fig, ax = plt.subplots(figsize=(14, 8))
    pts = [(r["Size"], r["Time_sec"]) for r in fib_rows if r["Algorithm"] == "FibMemoized"]
    if pts:
        xs, ys = zip(*sorted(pts))
        ax.plot(xs, ys, "s-", color="#ff7f0e", markersize=10, linewidth=3, label="FibMemoized")
    ax.set_xlabel("n (input size)")
    ax.set_ylabel("Time (sec)")
    ax.set_title(f"Memoized Fibonacci (linear scale) - {STUDENT}", fontsize=16, fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left", framealpha=0.9)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "fib_memoized_linear.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_tsp_full_range(tsp_rows):
    fig, ax = plt.subplots(figsize=(14, 8))
    colors = {"TSPBruteForce": "#1f77b4", "TSPHeldKarp": "#2ca02c"}
    markers = {"TSPBruteForce": "o", "TSPHeldKarp": "D"}
    for algo, label in [
        ("TSPBruteForce", "TSPBruteForce O(n!)"),
        ("TSPHeldKarp", "TSPHeldKarp O(n\u00b2\u00b72\u207f)"),
    ]:
        pts = [(r["Size"], r["Time_sec"]) for r in tsp_rows if r["Algorithm"] == algo]
        if pts:
            xs, ys = zip(*sorted(pts))
            ax.plot(xs, ys, marker=markers[algo], color=colors[algo],
                    markersize=10, label=label, linewidth=3)
    ax.set_xlabel("n (number of cities)")
    ax.set_ylabel("Time (sec)")
    ax.set_title(f"TSP Runtime Comparison - {STUDENT}", fontsize=16, fontweight="bold")
    ax.legend(loc="upper left", framealpha=0.9)
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "tsp_full_range.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_tsp_log_single(tsp_rows):
    fig, ax = plt.subplots(figsize=(14, 8))
    pts = [(r["Size"], r["Time_sec"]) for r in tsp_rows if r["Algorithm"] == "TSPBruteForce"]
    if pts:
        xs, ys = zip(*sorted(pts))
        ax.plot(xs, ys, "o-", color="#1f77b4", markersize=10, linewidth=3, label="TSPBruteForce")
    ax.set_xlabel("n (number of cities)")
    ax.set_ylabel("Time (sec)")
    ax.set_title(f"Brute Force TSP (log scale) - {STUDENT}", fontsize=16, fontweight="bold")
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3, which="both")
    ax.legend(loc="upper left", framealpha=0.9)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "tsp_log_single.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_tsp_raw_vs_averaged(tsp_rows):
    fig, ax = plt.subplots(figsize=(14, 8))
    size = 8
    pts = [r for r in tsp_rows if r["Algorithm"] == "TSPHeldKarp" and r["Size"] == size]
    if pts:
        times = [r["Time_sec"] for r in pts]
        avg = statistics.mean(times)
        trial_nums = list(range(1, len(times) + 1))
        ax.scatter(trial_nums, times, marker="x", color="gray", s=120, linewidths=2,
                    label=f"Raw trials (n={size})")
        ax.axhline(y=avg, color="#d62728", linestyle="-", linewidth=3,
                    label=f"Mean = {avg:.8f}s")
    ax.set_xlabel("Trial Number")
    ax.set_ylabel("Time (sec)")
    ax.set_title(f"Held-Karp at n={size}: Raw vs Averaged - {STUDENT}", fontsize=16, fontweight="bold")
    ax.grid(True, alpha=0.3)
    if pts:
        ax.legend(loc="best", framealpha=0.9)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "tsp_raw_vs_averaged.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def main():
    fib_rows = read_csv(os.path.join(RESULTS_DIR, "fib_results.csv"))
    tsp_rows = read_csv(os.path.join(RESULTS_DIR, "tsp_results.csv"))
    plot_fib_full_range(fib_rows)
    plot_fib_recursive_log(fib_rows)
    plot_fib_memoized_linear(fib_rows)
    plot_tsp_full_range(tsp_rows)
    plot_tsp_log_single(tsp_rows)
    plot_tsp_raw_vs_averaged(tsp_rows)
    print("All plots saved to", FIGURES_DIR)


if __name__ == "__main__":
    main()
