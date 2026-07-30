import csv
import os

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

RESULTS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "results", "sorting_results.csv"
)
FIGURES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "figures_1"
)
os.makedirs(FIGURES_DIR, exist_ok=True)

ALGO_LABELS = {
    "BubbleSort": "BubbleSort O(n\xb2)",
    "SelectionSort": "SelectionSort O(n\xb2)",
    "InsertionSort": "InsertionSort O(n\xb2)",
    "MergeSort": "MergeSort O(n log n)",
    "QuickSort": "QuickSort O(n log n)",
    "HeapSort": "HeapSort O(n log n)",
}

ALGO_ORDER = [
    "BubbleSort",
    "SelectionSort",
    "InsertionSort",
    "MergeSort",
    "QuickSort",
    "HeapSort",
]

ALGO_COLORS = {
    "BubbleSort": "#1f77b4",
    "SelectionSort": "#ff7f0e",
    "InsertionSort": "#2ca02c",
    "MergeSort": "#d62728",
    "QuickSort": "#9467bd",
    "HeapSort": "#8c564b",
}

ALGO_MARKERS = {
    "BubbleSort": "o",
    "SelectionSort": "s",
    "InsertionSort": "^",
    "MergeSort": "D",
    "QuickSort": "v",
    "HeapSort": "p",
}

STUDENT = "Prajwal Ghimire (22)"


def load_data():
    rows = []
    with open(RESULTS_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def numeric_or_none(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def avg_and_bounds(values):
    vals = [v for v in values if v is not None]
    if not vals:
        return None, None, None
    return sum(vals) / len(vals), min(vals), max(vals)


def get_algorithm_data(rows, algorithm, case=None):
    data = {}
    for row in rows:
        if row["Algorithm"] != algorithm:
            continue
        if case is not None and row["Case"] != case:
            continue
        size = int(row["Size"])
        t = numeric_or_none(row["Time_sec"])
        data.setdefault(size, []).append(t)
    return data


def plot_full_range(rows):
    fig, ax = plt.subplots(figsize=(14, 8))
    for alg in ALGO_ORDER:
        data = get_algorithm_data(rows, alg, case="Average")
        sizes = sorted(data.keys())
        means = []
        for s in sizes:
            m, _, _ = avg_and_bounds(data[s])
            means.append(m)
        ax.plot(sizes, means, marker=ALGO_MARKERS[alg], color=ALGO_COLORS[alg],
                markersize=8, label=ALGO_LABELS[alg])
    ax.set_xlabel("Input Size (n)")
    ax.set_ylabel("Time (seconds)")
    ax.set_title(f"Sorting Algorithm Comparison (Average Case) - {STUDENT}", fontsize=16, fontweight="bold")
    ax.legend(loc="upper left", framealpha=0.9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "sorting_full_range.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_zoomed(rows):
    fig, ax = plt.subplots(figsize=(14, 8))
    for alg in ALGO_ORDER:
        data = get_algorithm_data(rows, alg, case="Average")
        sizes = sorted(s for s in data if s <= 10000)
        means = []
        for s in sizes:
            m, _, _ = avg_and_bounds(data[s])
            means.append(m)
        ax.plot(sizes, means, marker=ALGO_MARKERS[alg], color=ALGO_COLORS[alg],
                markersize=10, label=ALGO_LABELS[alg])
    ax.set_xlabel("Input Size (n)")
    ax.set_ylabel("Time (seconds)")
    ax.set_xlim(0, 10000)
    ax.set_title(f"Sorting Algorithm Comparison (n \u2264 10000) - {STUDENT}", fontsize=16, fontweight="bold")
    ax.legend(loc="upper left", framealpha=0.9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "sorting_zoomed.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_best_avg_worst(rows):
    fig, ax = plt.subplots(figsize=(14, 8))
    styles = {"Best": (0, (5, 1)), "Average": (0, (1, 1)), "Worst": (0, (1, 1))}
    colors = {"InsertionSort": "#2ca02c", "SelectionSort": "#ff7f0e"}
    for alg in ("InsertionSort", "SelectionSort"):
        for case_name in ("Best", "Average", "Worst"):
            data = get_algorithm_data(rows, alg, case=case_name)
            sizes = sorted(data.keys())
            means = []
            for s in sizes:
                m, _, _ = avg_and_bounds(data[s])
                means.append(m)
            ls = "solid" if case_name == "Best" else ("dashed" if case_name == "Average" else "dotted")
            ax.plot(
                sizes, means,
                linestyle=ls, color=colors[alg],
                linewidth=2.5 if case_name != "Average" else 2,
                marker="." if case_name != "Average" else "^",
                markersize=10,
                label=f"{alg} ({case_name})",
            )
    ax.set_xlabel("Input Size (n)")
    ax.set_ylabel("Time (seconds)")
    ax.set_title(f"Best / Average / Worst Case Comparison - {STUDENT}", fontsize=16, fontweight="bold")
    ax.legend(loc="upper left", framealpha=0.9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "sorting_best_avg_worst.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_log_scale(rows):
    fig, ax = plt.subplots(figsize=(14, 8))
    for alg in ALGO_ORDER:
        data = get_algorithm_data(rows, alg, case="Average")
        sizes = sorted(data.keys())
        means = []
        for s in sizes:
            m, _, _ = avg_and_bounds(data[s])
            means.append(m if m is not None and m > 0 else None)
        ax.plot(sizes, means, marker=ALGO_MARKERS[alg], color=ALGO_COLORS[alg],
                markersize=8, label=ALGO_LABELS[alg])
    ax.set_yscale("log")
    ax.set_xlabel("Input Size (n)")
    ax.set_ylabel("Time (seconds) [log scale]")
    ax.set_title(f"Sorting Algorithm Comparison (Log Scale) - {STUDENT}", fontsize=16, fontweight="bold")
    ax.legend(loc="upper left", framealpha=0.9)
    ax.grid(True, alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "sorting_log_scale.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_shaded_band(rows):
    fig, ax = plt.subplots(figsize=(14, 8))
    data = get_algorithm_data(rows, "MergeSort", case="Average")
    sizes = sorted(data.keys())
    means, mins, maxs = [], [], []
    for s in sizes:
        m, lo, hi = avg_and_bounds(data[s])
        means.append(m)
        mins.append(lo)
        maxs.append(hi)

    ax.plot(sizes, means, "b-", linewidth=3, label="MergeSort Average")
    ax.fill_between(sizes, mins, maxs, alpha=0.3, color="b", label="Min-Max Range")
    ax.set_xlabel("Input Size (n)")
    ax.set_ylabel("Time (seconds)")
    ax.set_title(f"MergeSort Variation Across Trials - {STUDENT}", fontsize=16, fontweight="bold")
    ax.text(
        0.5, 0.95,
        "Mean over 5 random instances \u00b7 shaded band = min-max range",
        transform=ax.transAxes, ha="center", va="top",
        fontsize=12, style="italic",
    )
    ax.legend(loc="upper left", framealpha=0.9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "sorting_shaded_band.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_raw_vs_averaged(rows):
    fig, ax = plt.subplots(figsize=(14, 8))
    data = get_algorithm_data(rows, "InsertionSort", case="Average")
    size_1000_trials = [v for v in data.get(1000, []) if v is not None]
    trial_numbers = list(range(1, len(size_1000_trials) + 1))
    ax.scatter(
        trial_numbers, size_1000_trials,
        marker="x", color="gray", s=100, linewidths=2, label="Raw per-trial times",
    )
    if size_1000_trials:
        avg_val = sum(size_1000_trials) / len(size_1000_trials)
        ax.axhline(y=avg_val, color="#d62728", linestyle="-", linewidth=3,
                    label=f"Averaged (mean = {avg_val:.6f}s)")
    ax.set_xlabel("Trial Number")
    ax.set_ylabel("Time (seconds)")
    ax.set_title(f"Raw vs Averaged Times (InsertionSort, n=1000) - {STUDENT}", fontsize=16, fontweight="bold")
    ax.legend(loc="best", framealpha=0.9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "sorting_raw_vs_averaged.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def main():
    rows = load_data()
    plot_full_range(rows)
    plot_zoomed(rows)
    plot_best_avg_worst(rows)
    plot_log_scale(rows)
    plot_shaded_band(rows)
    plot_raw_vs_averaged(rows)
    print("All figures saved to", FIGURES_DIR)


if __name__ == "__main__":
    main()
