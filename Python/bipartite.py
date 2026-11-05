def is_bipartite(graph):
    """Return True if the undirected graph is bipartite."""
    n = len(graph)
    color = [-1] * n

    for start in range(n):
        if color[start] != -1:
            continue
        color[start] = 0
        queue = [start]
        head = 0

        while head < len(queue):
            u = queue[head]
            head += 1
            for v in graph[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    queue.append(v)
                elif color[v] == color[u]:
                    return False

    return True
