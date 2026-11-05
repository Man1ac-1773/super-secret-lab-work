def _push(heap, item):
    heap.append(item)
    i = len(heap) - 1
    while i > 0:
        parent = (i - 1) // 2
        if heap[parent][0] <= heap[i][0]:
            break
        heap[parent], heap[i] = heap[i], heap[parent]
        i = parent


def _pop(heap):
    last = heap.pop()
    if not heap:
        return last

    root = heap[0]
    heap[0] = last
    i = 0

    while True:
        left = 2 * i + 1
        right = left + 1
        smallest = i

        if left < len(heap) and heap[left][0] < heap[smallest][0]:
            smallest = left
        if right < len(heap) and heap[right][0] < heap[smallest][0]:
            smallest = right

        if smallest == i:
            break

        heap[i], heap[smallest] = heap[smallest], heap[i]
        i = smallest

    return root


def dijkstra_heap(graph, start):
    """Dijkstra with a manual binary heap: O((V + E) log V).

    graph[u] contains (v, weight) pairs. Weights must be non-negative.
    """
    n = len(graph)
    dist = [float("inf")] * n
    parent = [-1] * n
    dist[start] = 0

    heap = [(0, start)]

    while heap:
        d, u = _pop(heap)
        if d != dist[u]:
            continue

        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                _push(heap, (nd, v))

    return dist, parent


def dijkstra_heap_path(parent, start, target):
    if target != start and parent[target] == -1:
        return []

    path = []
    node = target
    while node != -1:
        path.append(node)
        if node == start:
            break
        node = parent[node]

    if not path or path[-1] != start:
        return []

    path.reverse()
    return path
