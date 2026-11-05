class _DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


def kruskal(n, edges):
    """Minimum spanning tree.

    edges is a list of (u, v, weight).
    Returns (total_weight, chosen_edges).
    """
    dsu = _DSU(n)
    chosen = []
    total = 0

    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if dsu.union(u, v):
            chosen.append((u, v, w))
            total += w
            if len(chosen) == n - 1:
                break

    return total, chosen
