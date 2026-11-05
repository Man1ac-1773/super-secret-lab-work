def dfs(graph, start):
    """Recursive DFS from one start vertex.

    Returns (order, parent, discover, finish).
    Colors: 0 = white, 1 = gray, 2 = black.
    """
    n = len(graph)
    color = [0] * n
    parent = [-1] * n
    discover = [0] * n
    finish = [0] * n
    order = []
    timer = 0

    def visit(u):
        nonlocal timer
        color[u] = 1
        discover[u] = timer
        timer += 1
        order.append(u)

        for v in graph[u]:
            if color[v] == 0:
                parent[v] = u
                visit(v)

        color[u] = 2
        finish[u] = timer
        timer += 1

    visit(start)
    return order, parent, discover, finish


def dfs_all(graph):
    """DFS over every component; returns (order, parent, components)."""
    n = len(graph)
    color = [0] * n
    parent = [-1] * n
    order = []
    components = []
    timer = 0

    def visit(u, comp):
        nonlocal timer
        color[u] = 1
        timer += 1
        order.append(u)
        comp.append(u)

        for v in graph[u]:
            if color[v] == 0:
                parent[v] = u
                visit(v, comp)

        color[u] = 2

    for s in range(n):
        if color[s] == 0:
            comp = []
            visit(s, comp)
            components.append(comp)

    return order, parent, components


def dfs_iterative(graph, start):
    """Iterative preorder DFS. Does not compute finish times."""
    n = len(graph)
    visited = [False] * n
    parent = [-1] * n
    order = []

    stack = [start]
    visited[start] = True

    while stack:
        u = stack.pop()
        order.append(u)

        for v in reversed(graph[u]):
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                stack.append(v)

    return order, parent
