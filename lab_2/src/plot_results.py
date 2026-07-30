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

RESULTS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "results"
)
FIGURES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "figures_2"
)
os.makedirs(FIGURES_DIR, exist_ok=True)

STUDENT = "Prajwal Ghimire (22)"


def _load_csv(path):
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def _numeric(v):
    try:
        return float(v)
    except (ValueError, TypeError):
        return None


def _group_by_size(rows, algorithm=None):
    data = {}
    for row in rows:
        if algorithm is not None and row["Algorithm"] != algorithm:
            continue
        size = int(row["Size"])
        t = _numeric(row["Time_sec"])
        if t is not None:
            data.setdefault(size, []).append(t)
    return data


def _mean_min_max(vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return None, None, None
    return sum(vals) / len(vals), min(vals), max(vals)


def plot_as_full_range():
    rows = _load_csv(os.path.join(RESULTS_DIR, "activity_results.csv"))
    fig, ax = plt.subplots(figsize=(14, 8))

    colors = {"BruteForce": "#1f77b4", "GreedyIterative": "#ff7f0e"}
    markers = {"BruteForce": "o", "GreedyIterative": "s"}

    for alg, label in [
        ("BruteForce", "Brute Force O(2\u207f n)"),
        ("GreedyIterative", "Greedy Iterative O(n log n)"),
    ]:
        data = _group_by_size(rows, alg)
        sizes = sorted(data)
        means = []
        for s in sizes:
            m, _, _ = _mean_min_max(data[s])
            means.append(m)
        ax.plot(sizes, means, marker=markers[alg], color=colors[alg],
                markersize=10, label=label, linewidth=3)

    ax.set_yscale("log")
    ax.set_xlabel("Number of Activities (n)")
    ax.set_ylabel("Time (seconds)")
    ax.set_title(f"Activity Selection - Algorithm Comparison - {STUDENT}", fontsize=16, fontweight="bold")
    ax.legend(loc="upper left", framealpha=0.9)
    ax.grid(True, alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "as_full_range.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_as_quality():
    rows = _load_csv(os.path.join(RESULTS_DIR, "activity_quality.csv"))
    fig, ax = plt.subplots(figsize=(14, 8))

    data = {}
    for row in rows:
        size = int(row["Size"])
        q = _numeric(row["QualityPct"])
        if q is not None:
            data.setdefault(size, []).append(q)

    sizes = sorted(data)
    means, mins, maxs = [], [], []
    for s in sizes:
        m, lo, hi = _mean_min_max(data[s])
        means.append(m)
        mins.append(lo)
        maxs.append(hi)

    ax.plot(sizes, means, "g-", linewidth=3, label="Mean Quality")
    ax.fill_between(sizes, mins, maxs, alpha=0.25, color="g", label="Min-Max Range")
    ax.axhline(y=100, color="gray", linestyle="--", linewidth=2, label="Optimal (100%)")

    ax.set_xlabel("Number of Activities (n)")
    ax.set_ylabel("Quality (% of Optimal)")
    ax.set_title(f"Activity Selection - Solution Quality vs Optimal - {STUDENT}", fontsize=16, fontweight="bold")
    ax.set_ylim(95, 105)
    ax.legend(loc="best", framealpha=0.9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "as_quality.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_k_full_range():
    rows = _load_csv(os.path.join(RESULTS_DIR, "knapsack_results.csv"))
    fig, ax = plt.subplots(figsize=(14, 8))

    colors = {"BruteForce": "#1f77b4", "GreedyRatio": "#2ca02c"}
    markers = {"BruteForce": "o", "GreedyRatio": "^"}

    for alg, label in [
        ("BruteForce", "Brute Force O(2\u207f)"),
        ("GreedyRatio", "Greedy Ratio O(n log n)"),
    ]:
        data = _group_by_size(rows, alg)
        sizes = sorted(data)
        means = []
        for s in sizes:
            m, _, _ = _mean_min_max(data[s])
            means.append(m)
        ax.plot(sizes, means, marker=markers[alg], color=colors[alg],
                markersize=10, label=label, linewidth=3)

    ax.set_yscale("log")
    ax.set_xlabel("Number of Items (n)")
    ax.set_ylabel("Time (seconds)")
    ax.set_title(f"0/1 Knapsack - Algorithm Comparison - {STUDENT}", fontsize=16, fontweight="bold")
    ax.legend(loc="upper left", framealpha=0.9)
    ax.grid(True, alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "k_full_range.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_k_quality():
    rows = _load_csv(os.path.join(RESULTS_DIR, "knapsack_quality.csv"))
    fig, ax = plt.subplots(figsize=(14, 8))

    data = {}
    for row in rows:
        size = int(row["Size"])
        q = _numeric(row["QualityPct"])
        if q is not None:
            data.setdefault(size, []).append(q)

    sizes = sorted(data)
    means, mins, maxs = [], [], []
    for s in sizes:
        m, lo, hi = _mean_min_max(data[s])
        means.append(m)
        mins.append(lo)
        maxs.append(hi)

    ax.plot(sizes, means, "b-", linewidth=3, label="Mean Quality")
    ax.fill_between(sizes, mins, maxs, alpha=0.25, color="b", label="Min-Max Range")
    ax.axhline(y=100, color="gray", linestyle="--", linewidth=2, label="Optimal (100%)")

    ax.set_xlabel("Number of Items (n)")
    ax.set_ylabel("Quality (% of Optimal)")
    ax.set_title(f"0/1 Knapsack - Greedy Solution Quality vs Optimal - {STUDENT}", fontsize=16, fontweight="bold")
    ax.set_ylim(50, 105)
    ax.legend(loc="best", framealpha=0.9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "k_quality.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_as_raw_vs_averaged():
    rows = _load_csv(os.path.join(RESULTS_DIR, "activity_results.csv"))
    fig, ax = plt.subplots(figsize=(14, 8))

    target_size = 14
    data = _group_by_size(rows, "GreedyIterative")
    trials = data.get(target_size, [])
    if not trials:
        target_size = 12
        trials = data.get(target_size, [])

    trial_numbers = list(range(1, len(trials) + 1))
    ax.scatter(
        trial_numbers, trials,
        marker="x", color="gray", s=120, linewidths=2, label="Raw per-trial times",
    )
    if trials:
        avg_val = sum(trials) / len(trials)
        ax.axhline(y=avg_val, color="#d62728", linestyle="-", linewidth=3,
                    label=f"Averaged (mean = {avg_val:.6f}s)")

    ax.set_xlabel("Trial Number")
    ax.set_ylabel("Time (seconds)")
    ax.set_title(f"Raw vs Averaged Times (Greedy Iterative, n={target_size}) - {STUDENT}", fontsize=16, fontweight="bold")
    ax.legend(loc="best", framealpha=0.9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "as_raw_vs_averaged.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_overlay_log_scale():
    as_rows = _load_csv(os.path.join(RESULTS_DIR, "activity_results.csv"))
    kp_rows = _load_csv(os.path.join(RESULTS_DIR, "knapsack_results.csv"))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

    for ax, title, data_rows, alg1, alg2, label1, label2, xlbl in [
        (ax1, f"Activity Selection - {STUDENT}", as_rows,
         "BruteForce", "GreedyIterative",
         "Brute Force O(2\u207f n)", "Greedy Iterative O(n log n)", "Activities (n)"),
        (ax2, f"0/1 Knapsack - {STUDENT}", kp_rows,
         "BruteForce", "GreedyRatio",
         "Brute Force O(2\u207f)", "Greedy Ratio O(n log n)", "Items (n)"),
    ]:
        colors = {"BruteForce": "#1f77b4", "GreedyIterative": "#ff7f0e",
                   "GreedyRatio": "#2ca02c"}
        markers = {"BruteForce": "o", "GreedyIterative": "s", "GreedyRatio": "^"}
        for alg, label in [(alg1, label1), (alg2, label2)]:
            data = _group_by_size(data_rows, alg)
            sizes = sorted(data)
            means = []
            for s in sizes:
                m, _, _ = _mean_min_max(data[s])
                means.append(m)
            ax.plot(sizes, means, marker=markers[alg], color=colors[alg],
                    markersize=10, label=label, linewidth=3)

        ax.set_yscale("log")
        ax.set_xlabel(xlbl)
        ax.set_ylabel("Time (seconds)")
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.legend(fontsize=10, loc="upper left", framealpha=0.9)
        ax.grid(True, alpha=0.3, which="both")

    fig.suptitle("Brute Force vs Greedy - Orders of Magnitude Gap", fontsize=17, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "overlay_log_scale.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def main():
    plot_as_full_range()
    plot_as_quality()
    plot_k_full_range()
    plot_k_quality()
    plot_as_raw_vs_averaged()
    plot_overlay_log_scale()
    print("All figures saved to", FIGURES_DIR)


if __name__ == "__main__":
    main()
