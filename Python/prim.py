def prim(graph, start=0):
    """Minimum spanning tree for a weighted undirected graph.

    graph[u] is a list of (v, weight) pairs.
    Returns (total_weight, chosen_edges). Graph is assumed connected.
    """
    n = len(graph)
    if n == 0:
        return 0, []

    inf = float("inf")
    best = [inf] * n
    parent = [-1] * n
    used = [False] * n
    chosen = []
    total = 0

    best[start] = 0

    for _ in range(n):
        u = -1
        for i in range(n):
            if not used[i] and (u == -1 or best[i] < best[u]):
                u = i

        if u == -1 or best[u] == inf:
            break

        used[u] = True
        total += best[u]
        if parent[u] != -1:
            chosen.append((parent[u], u, best[u]))

        for v, w in graph[u]:
            if not used[v] and w < best[v]:
                best[v] = w
                parent[v] = u

    return total, chosen
