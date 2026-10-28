def clarke_wright(dist, demand, capacity):
    """savings heauristic for the capacitated VPR. dist[0] is the depot."""
    n = len(dist)
    # Step 1: one out-and-back trip per customer
    routes = {c: [c] for c in range(1, n)}
    load = {c: demand[c] for c in range(1, n)}

    def route_of(c):
        return next((k for k, r in routes.items() if c in r), None)

    # Step 2: how much is saved by serving i and j on one trip instead of two
    savings = sorted(
        (
            (dist[0][i] + dist[0][j] - dist[i][j], i, j)
            for i in range(1, n) for j in range(i + 1, n)
            ),
        reverse=True
    )

    # Step 3: merge greedily, best saving first
    for _, i, j in savings:
        ri, rj = route_of(i), route_of(j)
        if ri is None or rj is None or ri == rj:
            continue
        if load[ri] + load[rj] > capacity:
            continue # the constraint that makes this VRP and not TSP


        a, b = routes[ri], routes[rj]
        # i and j each have to sit at an end of their own route
        if a[-1] == i and b[0] == j: merged = a + b
        elif b[-1] == j and a[0] == i: merged = b + a
        elif a[0] == i and b[0] == j: merged = a[::-1] + b
        elif a[-1] == i and b[-1] == j: merged = a + b[::-1]
        else:                           continue

        routes[ri], load[ri] = merged, load[ri] + load[rj]
        del routes[rj], load[rj]

    return [[0] + r + [0] for r in routes.values()]


# A depot at (node 0) and five customers (nodes 1-5).
dist = [
    [0, 5, 4, 5, 4, 5],
    [5, 0, 3, 5, 9, 6],
    [4, 3, 0, 7, 8, 3],
    [5, 5, 7,  0, 8, 10],
    [4, 9, 8,  8, 0,  8],
    [5, 6, 3, 10, 8,  0],
]
demand = [0, 4, 3, 5, 3, 4] # depot first, then one figure per customer

routes = clarke_wright(dist, demand, capacity=10)
print(routes)
#Expected output:
# [[0, 1, 3, 0], [0, 2, 5, 4, 0]]
#
# Vehicle loads: 9 and 10
# Total distance: 34
# Original distance: 46
# Distance reduction: approximately 26.1%