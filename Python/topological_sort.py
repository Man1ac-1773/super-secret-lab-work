def topological_sort(graph):
    """Kahn's algorithm. Returns a topological order, or [] if a cycle exists."""
    n = len(graph)
    indegree = [0] * n
    for u in range(n):
        for v in graph[u]:
            indegree[v] += 1

    queue = [u for u in range(n) if indegree[u] == 0]
    head = 0
    order = []

    while head < len(queue):
        u = queue[head]
        head += 1
        order.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)

    if len(order) != n:
        return []
    return order


def topological_sort_dfs(graph):
    """DFS version: reverse finish order. Returns [] if a cycle exists."""
    n = len(graph)
    color = [0] * n
    order = []
    cycle = False

    def visit(u):
        nonlocal cycle
        color[u] = 1
        for v in graph[u]:
            if color[v] == 1:
                cycle = True
                return
            if color[v] == 0:
                visit(v)
                if cycle:
                    return
        color[u] = 2
        order.append(u)

    for u in range(n):
        if color[u] == 0:
            visit(u)
            if cycle:
                return []

    order.reverse()
    return order
