def dijkstra(graph, start):
    """Single-source shortest paths with non-negative weights.

    graph[u] is a list of (v, weight) pairs.
    Returns (dist, parent). Unreachable vertices have dist = inf.
    This simple version is O(V^2); use a heap for very large sparse graphs.
    """
    n = len(graph)
    inf = float("inf")
    dist = [inf] * n
    parent = [-1] * n
    used = [False] * n

    dist[start] = 0

    for _ in range(n):
        u = -1
        for i in range(n):
            if not used[i] and (u == -1 or dist[i] < dist[u]):
                u = i

        if u == -1 or dist[u] == inf:
            break

        used[u] = True

        for v, w in graph[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u

    return dist, parent


def dijkstra_path(parent, start, target):
    """Rebuild a shortest path, or [] if the target is unreachable."""
    if target == start:
        return [start]
    if parent[target] == -1:
        return []

    path = []
    cur = target
    while cur != -1:
        path.append(cur)
        if cur == start:
            path.reverse()
            return path
        cur = parent[cur]
    return []


def dijkstra_to_target(graph, start, target):
    """Stop as soon as target is finalized; returns its distance or -1."""
    n = len(graph)
    inf = float("inf")
    dist = [inf] * n
    used = [False] * n
    dist[start] = 0

    for _ in range(n):
        u = -1
        for i in range(n):
            if not used[i] and (u == -1 or dist[i] < dist[u]):
                u = i

        if u == -1 or dist[u] == inf:
            break
        if u == target:
            return dist[u]

        used[u] = True

        for v, w in graph[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd

    return -1
