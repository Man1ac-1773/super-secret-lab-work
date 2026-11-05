def floyd_warshall(matrix):
    """All-pairs shortest paths.

    matrix[i][j] is the edge weight, 0 on the diagonal, inf if no edge.
    Returns a new distance matrix.
    """
    n = len(matrix)
    dist = [row[:] for row in matrix]

    for k in range(n):
        for i in range(n):
            if dist[i][k] == float("inf"):
                continue
            for j in range(n):
                nd = dist[i][k] + dist[k][j]
                if nd < dist[i][j]:
                    dist[i][j] = nd

    return dist


def floyd_warshall_paths(matrix):
    """Return (dist, nxt) for path reconstruction.

    Path from i to j: start at i, then nxt[i][j], and so on.
    """
    n = len(matrix)
    inf = float("inf")
    dist = [row[:] for row in matrix]
    nxt = [[-1] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j and dist[i][j] != inf:
                nxt[i][j] = j

    for k in range(n):
        for i in range(n):
            if dist[i][k] == inf:
                continue
            for j in range(n):
                nd = dist[i][k] + dist[k][j]
                if nd < dist[i][j]:
                    dist[i][j] = nd
                    nxt[i][j] = nxt[i][k]

    return dist, nxt


def has_negative_cycle(dist):
    """A negative cycle exists iff some dist[i][i] is negative."""
    for i in range(len(dist)):
        if dist[i][i] < 0:
            return True
    return False


def rebuild_path(nxt, start, target):
    """Rebuild a path from the nxt matrix; [] if unreachable."""
    if start == target:
        return [start]
    if nxt[start][target] == -1:
        return []

    path = [start]
    cur = start
    while cur != target:
        cur = nxt[cur][target]
        if cur == -1:
            return []
        path.append(cur)
        if len(path) > len(nxt) + 1:
            return []
    return path
