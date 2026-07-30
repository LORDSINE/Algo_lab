def activity_brute_force(activities):
    n = len(activities)
    max_count = 0
    for mask in range(1 << n):
        selected = []
        for i in range(n):
            if mask & (1 << i):
                selected.append(activities[i])
        compatible = True
        for i in range(len(selected)):
            for j in range(i + 1, len(selected)):
                s1, f1 = selected[i]
                s2, f2 = selected[j]
                if s1 < f2 and s2 < f1:
                    compatible = False
                    break
            if not compatible:
                break
        if compatible:
            max_count = max(max_count, len(selected))
    return max_count


def activity_greedy_iterative(activities):
    sorted_act = sorted(activities, key=lambda x: x[1])
    count = 0
    last_finish = 0
    for s, f in sorted_act:
        if s >= last_finish:
            count += 1
            last_finish = f
    return count


def activity_greedy_recursive(activities, k, n):
    m = k + 1
    while m < n:
        start_m = activities[m][0]
        finish_k = 0 if k == -1 else activities[k][1]
        if start_m >= finish_k:
            break
        m += 1
    if m < n:
        return 1 + activity_greedy_recursive(activities, m, n)
    return 0


def knapsack_brute_force(values, weights, capacity):
    n = len(values)
    max_value = 0
    for mask in range(1 << n):
        total_weight = 0
        total_value = 0
        for i in range(n):
            if mask & (1 << i):
                total_weight += weights[i]
                total_value += values[i]
        if total_weight <= capacity:
            max_value = max(max_value, total_value)
    return max_value


def knapsack_greedy_ratio(values, weights, capacity):
    n = len(values)
    items = [(values[i], weights[i], i, values[i] / weights[i]) for i in range(n)]
    items.sort(key=lambda x: x[3], reverse=True)
    total_value = 0
    total_weight = 0
    selected_indices = []
    for v, w, idx, _ in items:
        if total_weight + w <= capacity:
            total_weight += w
            total_value += v
            selected_indices.append(idx)
    return total_value, total_weight, selected_indices


if __name__ == "__main__":
    print("=== Activity Selection ===")
    acts = [(1, 3), (2, 5), (3, 6), (5, 7), (6, 8)]
    print(f"  Activities: {acts}")
    print(f"  Brute Force:          {activity_brute_force(acts)}")
    print(f"  Greedy Iterative:     {activity_greedy_iterative(acts)}")
    print(f"  Greedy Recursive:     {activity_greedy_recursive(sorted(acts, key=lambda x: x[1]), -1, len(acts))}")

    print("\n=== 0/1 Knapsack ===")
    values = [60, 100, 120]
    weights = [10, 20, 30]
    capacity = 50
    print(f"  Values:  {values}")
    print(f"  Weights: {weights}")
    print(f"  Capacity: {capacity}")
    print(f"  Brute Force:          {knapsack_brute_force(values, weights, capacity)}")
    gv, gw, gi = knapsack_greedy_ratio(values, weights, capacity)
    print(f"  Greedy Ratio:         value={gv}, weight={gw}, items={gi}")
