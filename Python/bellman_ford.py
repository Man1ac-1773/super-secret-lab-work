def bellman_ford(n, edges, start):
    """Single-source shortest paths, including negative edges.

    edges is a list of (u, v, weight) directed edges.
    Returns (dist, parent), or None if a negative cycle is reachable.
    """
    inf = float("inf")
    dist = [inf] * n
    parent = [-1] * n
    dist[start] = 0

    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
        if not changed:
            break

    for u, v, w in edges:
        if dist[u] != inf and dist[u] + w < dist[v]:
            return None

    return dist, parent


def bellman_ford_path(parent, start, target):
    """Rebuild a path from the parent array, or [] if unreachable."""
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


def bellman_ford_undirected(n, edges, start):
    """Convenience wrapper: input (u, v, w) undirected edges."""
    directed = []
    for u, v, w in edges:
        directed.append((u, v, w))
        directed.append((v, u, w))
    return bellman_ford(n, directed, start)
