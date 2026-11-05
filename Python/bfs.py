def bfs(graph, start):
    """Return (dist, parent, order) for an unweighted graph."""
    n = len(graph)
    dist = [-1] * n
    parent = [-1] * n
    order = []

    dist[start] = 0
    queue = [start]
    head = 0

    while head < len(queue):
        u = queue[head]
        head += 1
        order.append(u)

        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                parent[v] = u
                queue.append(v)

    return dist, parent, order


def bfs_path(parent, start, target):
    """Rebuild one shortest path from start to target, or [] if unreachable."""
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


def multi_source_bfs(graph, sources):
    """Distance to the nearest source."""
    n = len(graph)
    dist = [-1] * n
    queue = []
    head = 0

    for s in sources:
        dist[s] = 0
        queue.append(s)

    while head < len(queue):
        u = queue[head]
        head += 1
        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)

    return dist


def grid_bfs(grid, start, target):
    """Shortest path length on a grid; '#' is blocked. Returns -1 if no path."""
    rows = len(grid)
    cols = len(grid[0])
    sr, sc = start
    tr, tc = target

    if not (0 <= sr < rows and 0 <= sc < cols):
        return -1
    if not (0 <= tr < rows and 0 <= tc < cols):
        return -1
    if grid[sr][sc] == "#" or grid[tr][tc] == "#":
        return -1

    dist = [[-1] * cols for _ in range(rows)]
    dist[sr][sc] = 0
    queue = [(sr, sc)]
    head = 0

    while head < len(queue):
        r, c = queue[head]
        head += 1
        if (r, c) == (tr, tc):
            return dist[r][c]

        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] != "#" and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    queue.append((nr, nc))

    return -1
