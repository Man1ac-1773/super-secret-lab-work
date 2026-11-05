def connected_components(graph):
    """Return a list of components; each component is a list of vertices."""
    n = len(graph)
    seen = [False] * n
    components = []

    def visit(u, comp):
        seen[u] = True
        comp.append(u)
        for v in graph[u]:
            if not seen[v]:
                visit(v, comp)

    for u in range(n):
        if not seen[u]:
            comp = []
            visit(u, comp)
            components.append(comp)

    return components
