import itertools


def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_memoized(n, memo=None):
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fib_memoized(n - 1, memo) + fib_memoized(n - 2, memo)
    return memo[n]


def tsp_brute_force(dist_matrix):
    n = len(dist_matrix)
    cities = list(range(1, n))
    min_cost = float('inf')
    best_tour = None
    for perm in itertools.permutations(cities):
        tour = [0] + list(perm)
        cost = 0
        for i in range(n):
            cost += dist_matrix[tour[i]][tour[(i + 1) % n]]
        if cost < min_cost:
            min_cost = cost
            best_tour = tour
    return min_cost, best_tour


def tsp_held_karp(dist_matrix):
    n = len(dist_matrix)
    dp = {}
    for i in range(1, n):
        mask = 1 | (1 << i)
        dp[(mask, i)] = (dist_matrix[0][i], 0)
    for mask in range(1, 1 << n):
        if not (mask & 1):
            continue
        for last in range(1, n):
            if not (mask & (1 << last)):
                continue
            key = (mask, last)
            if key not in dp:
                continue
            cur_cost, _ = dp[key]
            for nxt in range(1, n):
                if mask & (1 << nxt):
                    continue
                new_mask = mask | (1 << nxt)
                new_key = (new_mask, nxt)
                new_cost = cur_cost + dist_matrix[last][nxt]
                if new_key not in dp or new_cost < dp[new_key][0]:
                    dp[new_key] = (new_cost, last)
    full_mask = (1 << n) - 1
    best_cost = float('inf')
    best_last = -1
    for last in range(1, n):
        key = (full_mask, last)
        if key in dp:
            total = dp[key][0] + dist_matrix[last][0]
            if total < best_cost:
                best_cost = total
                best_last = last
    tour = [0]
    mask = full_mask
    last = best_last
    while last != 0:
        tour.append(last)
        _, prev = dp[(mask, last)]
        mask ^= (1 << last)
        last = prev
    tour.append(0)
    return best_cost, tour[::-1]


if __name__ == "__main__":
    print("=== Fibonacci ===")
    for n in [5, 10, 15]:
        print(f"  fib_recursive({n:2d}) = {fib_recursive(n)}")
        print(f"  fib_memoized({n:2d})  = {fib_memoized(n)}")

    print("\n=== TSP ===")
    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]
    bf_cost, bf_tour = tsp_brute_force(dist)
    hk_cost, hk_tour = tsp_held_karp(dist)
    print(f"  Distance matrix: 4 cities")
    print(f"  Brute Force: cost={bf_cost}, tour={bf_tour}")
    print(f"  Held-Karp:   cost={hk_cost}, tour={hk_tour}")
