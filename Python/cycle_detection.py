def has_cycle_undirected(graph):
    """Cycle detection in an undirected graph (no parallel edges)."""
    n = len(graph)
    visited = [False] * n

    def visit(u, parent):
        visited[u] = True
        for v in graph[u]:
            if not visited[v]:
                if visit(v, u):
                    return True
            elif v != parent:
                return True
        return False

    for u in range(n):
        if not visited[u]:
            if visit(u, -1):
                return True
    return False


def has_cycle_directed(graph):
    """Cycle detection in a directed graph using three colours."""
    n = len(graph)
    color = [0] * n

    def visit(u):
        color[u] = 1
        for v in graph[u]:
            if color[v] == 1:
                return True
            if color[v] == 0 and visit(v):
                return True
        color[u] = 2
        return False

    for u in range(n):
        if color[u] == 0 and visit(u):
            return True
    return False
