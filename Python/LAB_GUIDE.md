# CS2101 Lab Guide — BFS, DFS, Dijkstra, KMP, Rabin-Karp

This guide covers the **confirmed lab scope** only:

- BFS
- DFS
- Dijkstra
- KMP
- Rabin-Karp

The finite-automaton and Boyer-Moore files are included as background, but they are
not part of the confirmed string-matching scope.

The code lives in this folder. Each file is standalone: plain functions, no imports,
no `if __name__ == "__main__"`, and no external dependencies.

## Shared conventions

- Vertices are `0 .. n-1` internally. Convert 1-indexed input on read.
- Unweighted graph: `graph[u]` is a list of neighbours.
- Weighted graph: `graph[u]` is a list of `(v, weight)` pairs.
- `float("inf")` means unreachable.
- Path helpers take the `parent` array returned by the search.
- String indices are 0-based.

Typical input parsing:

```python
import sys

def read_unweighted():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    n = next(it)
    m = next(it)
    graph = [[] for _ in range(n)]
    for _ in range(m):
        u = next(it) - 1
        v = next(it) - 1
        graph[u].append(v)
        graph[v].append(u)      # omit for a directed graph
    return graph
```

For weighted graphs, append `(v, w)` instead of `v`.

---

# 1. BFS — Breadth-First Search

## What it solves

BFS finds the path with the **fewest edges** from a source to every reachable vertex.
That is a shortest path only when every edge has the same cost. If edges have different
weights, use Dijkstra or Bellman-Ford instead.

## Core idea

Explore in layers:

1. Put the source in a queue with distance 0.
2. Pop the oldest vertex.
3. For each unvisited neighbour, set its distance to `dist[u] + 1`, record its parent,
   and enqueue it.
4. Repeat until the queue is empty.

The key invariant is that the queue always contains vertices in non-decreasing distance
order. The first time a vertex is discovered is therefore via a shortest unweighted path.

## Code walkthrough — `bfs.py`

### `bfs(graph, start)`

```python
dist = [-1] * n
parent = [-1] * n
order = []
dist[start] = 0
queue = [start]
head = 0
```

- `dist[v] == -1` doubles as the unvisited marker.
- `head` avoids `pop(0)`, which would be `O(n)` per pop; the list grows and `head`
  walks forward, so the queue is amortised `O(1)`.
- `order` records the dequeue order, which is the BFS visit order.

The relaxation step:

```python
for v in graph[u]:
    if dist[v] == -1:
        dist[v] = dist[u] + 1
        parent[v] = u
        queue.append(v)
```

Mark the vertex **when it is enqueued**, not when it is popped. If you mark on pop, the
same vertex can be enqueued several times and its distance can be overwritten.

### `bfs_path(parent, start, target)`

Walk backwards from `target`:

```python
cur = target
while cur != -1:
    path.append(cur)
    if cur == start:
        path.reverse()
        return path
    cur = parent[cur]
return []
```

The `parent[target] == -1` check catches most unreachable targets. The loop also returns
`[]` if the parent chain does not reach `start`, which protects against malformed input.

### `multi_source_bfs(graph, sources)`

All sources start at distance 0 and are enqueued together. The result is the distance to
the **nearest** source. This is the standard trick for:

- nearest exit,
- nearest police station or hospital,
- rotting oranges,
- fire spread,
- multi-source flood fill.

It returns only `dist`, because a single parent tree is less meaningful when there are
several sources.

### `grid_bfs(grid, start, target)`

A grid is an implicit graph. Each cell has up to four neighbours:

```python
for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
    nr, nc = r + dr, c + dc
```

The function:

- checks that start and target are inside the grid,
- treats `#` as blocked,
- uses a 2D `dist` array as the visited marker,
- returns `-1` if the target is unreachable.

No adjacency list is built, which keeps memory at `O(rows * cols)`.

## Complexity

| Representation | Time | Space |
|---|---:|---:|
| Adjacency list | `O(V + E)` | `O(V)` |
| Adjacency matrix | `O(V^2)` | `O(V)` extra |

## Use cases

- Shortest path in an unweighted graph.
- Minimum moves in a grid or maze.
- Word ladder: each word is a vertex, one-letter changes are edges.
- Social-network degrees of separation.
- Multi-source spread problems.
- Bipartite checking: colour the graph in two colours while traversing.
- Connected components.
- Level-order traversal of a tree.
- Web crawling and peer-to-peer discovery, where you want nearby nodes first.

## Common mistakes

- Using BFS on a weighted graph. It minimises edge count, not total weight.
- Marking visited when popping instead of when enqueueing.
- Forgetting disconnected components: one `bfs` call only covers the source component.
- Reconstructing a path without checking reachability.
- Mixing 0-indexed and 1-indexed vertices.

## Lab checklist

- [ ] Is the graph unweighted?
- [ ] Is it directed or undirected?
- [ ] Are you asked for distance, path, visit order, or count?
- [ ] Did you mark on enqueue?
- [ ] Did you loop over all components if the graph may be disconnected?

---

# 2. DFS — Depth-First Search

## What it solves

DFS explores as deep as possible before backtracking. It is the right tool when the
structure of the search matters: cycles, ancestry, finish order, or exhaustive
exploration.

DFS does **not** compute shortest paths.

## Core idea

Use recursion or an explicit stack. With recursion, colour each vertex:

- **white**: unvisited,
- **gray**: currently on the recursion stack,
- **black**: finished.

A directed graph has a cycle exactly when DFS finds an edge to a gray vertex. An
undirected graph has a cycle when a visited neighbour is not the parent.

## Code walkthrough — `dfs.py`

### `dfs(graph, start)`

Returns `(order, parent, discover, finish)`.

```python
def visit(u):
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
```

- `discover[u]` is the time the vertex turns gray.
- `finish[u]` is the time it turns black.
- The interval `[discover[u], finish[u]]` is the DFS interval for `u`.
- `order` is preorder: a vertex is appended before its descendants.

With timestamps you can classify edges:

| Edge type | Condition |
|---|---|
| Tree edge | `v` was white when explored |
| Back edge | `v` is gray |
| Forward edge | `v` is black and `discover[u] < discover[v]` |
| Cross edge | `v` is black and `discover[v] < discover[u]` |

Only back edges indicate a directed cycle.

### `dfs_all(graph)`

Runs DFS from every unvisited vertex, so it covers disconnected graphs. It returns the
preorder, the parent array, and a list of components.

This is the version to use for:

- counting connected components,
- labelling components,
- checking whether an undirected graph is connected.

### `dfs_iterative(graph, start)`

Uses an explicit stack and returns `(order, parent)`. It computes preorder only; it does
not compute finish times, so it cannot classify edges or produce a topological order by
itself.

Neighbours are pushed in reverse order:

```python
for v in reversed(graph[u]):
    if not visited[v]:
        visited[v] = True
        parent[v] = u
        stack.append(v)
```

That keeps the visit order consistent with the recursive version for ordered adjacency
lists.

## Complexity

`O(V + E)` time with adjacency lists, `O(V)` space for colours, parents, and the stack.

## Use cases

- Cycle detection in directed and undirected graphs.
- Topological sorting of a DAG: reverse the finish order.
- Connected components.
- Bridges and articulation points.
- Maze solving and path existence.
- Backtracking search: N-Queens, Sudoku, subset sum, Hamiltonian cycle.
- Dependency resolution: course prerequisites, build systems, package managers.
- Flood fill when you do not need shortest distances.

## Common mistakes

- Using DFS for shortest paths.
- Using the undirected parent rule on a directed graph, or vice versa.
- Forgetting the gray state, which is what detects directed cycles.
- Assuming DFS order is unique; it depends on adjacency-list order.
- Blowing Python's recursion limit on a long path. Use `dfs_iterative` or raise the limit
  only when you understand the risk.
- Producing a topological order from a graph with a cycle.

## Lab checklist

- [ ] Directed or undirected?
- [ ] Do you need cycle detection, components, or topological order?
- [ ] Did you handle disconnected components?
- [ ] Is the graph a DAG before you output a topological order?
- [ ] Do you need finish times, or only preorder?

---

# 3. Dijkstra — Non-Negative Weighted Shortest Paths

## What it solves

Dijkstra computes the minimum-cost path from one source to every vertex when all edge
weights are non-negative. It is the weighted counterpart of BFS.

## Core idea

Maintain a set of **settled** vertices whose shortest distance is final. Repeatedly:

1. Pick the unsettled vertex with the smallest tentative distance.
2. Settle it.
3. Relax its outgoing edges: if `dist[u] + w < dist[v]`, improve `dist[v]`.

The correctness argument is the greedy one: because all weights are non-negative, no
future path through a farther vertex can improve the closest unsettled vertex.

## Code walkthrough — `dijkstra.py`

### `dijkstra(graph, start)`

This is the simple `O(V^2)` array version.

```python
for _ in range(n):
    u = -1
    for i in range(n):
        if not used[i] and (u == -1 or dist[i] < dist[u]):
            u = i

    if u == -1 or dist[u] == inf:
        break

    used[u] = True

    for v, w in graph[u]:
        nd = dist[u] + w
        if nd < dist[v]:
            dist[v] = nd
            parent[v] = u
```

Key points:

- The inner selection loop scans all vertices, which is why it is `O(V^2)`.
- `used[u] = True` means `dist[u]` is final.
- `if dist[u] == inf: break` stops when the remaining vertices are unreachable.
- `parent[v] = u` stores the predecessor for path reconstruction.

### `dijkstra_path(parent, start, target)`

Walks backwards from `target` and reverses the result. It returns `[]` if the target was
never reached.

### `dijkstra_to_target(graph, start, target)`

Stops as soon as `target` is selected as the minimum unsettled vertex. At that moment its
distance is final, so you do not need to process the rest of the graph.

Use this when the lab asks for one destination rather than all distances.

## The heap version — `dijkstra_heap.py`

The array version is simple and fine for small graphs. For large sparse graphs, use the
manual binary heap version:

```python
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
```

- `_push` and `_pop` implement a min-heap without importing `heapq`.
- The heap may contain several entries for the same vertex.
- `if d != dist[u]: continue` discards stale entries. This is the standard “lazy
  decrease-key” trick.
- Complexity is `O((V + E) log V)`.

## Complexity

| Version | Time | Space | Use when |
|---|---:|---:|---|
| Array | `O(V^2)` | `O(V)` | small or dense graphs |
| Binary heap | `O((V + E) log V)` | `O(V + E)` | large sparse graphs |

## Use cases

- Road networks and navigation.
- Network routing where costs are non-negative.
- Game pathfinding on weighted terrain.
- Flight or delivery costs where no edge is negative.
- Any “cheapest path” problem with non-negative weights.

## Common mistakes

- Using Dijkstra with negative edges. It can settle the wrong vertex and return a wrong
  answer; use Bellman-Ford.
- Forgetting to skip stale heap entries.
- Relaxing edges from a vertex that is already used in the array version.
- Returning `inf` as if it were a real distance.
- Forgetting that `parent` is only meaningful for reachable vertices.

## Lab checklist

- [ ] Are all weights non-negative?
- [ ] Do you need all distances or one target?
- [ ] Is the graph sparse enough to justify the heap version?
- [ ] Did you handle unreachable vertices?
- [ ] Do you need the path or only the distance?

---

# 4. KMP — Knuth-Morris-Pratt

## What it solves

KMP finds every occurrence of a pattern in a text in `O(n + m)` time, including
overlapping occurrences. It never rechecks a text character that has already been
matched.

## Core idea

Precompute how much of the pattern can be reused after a mismatch. The prefix function
`pi[i]` is the length of the longest **proper** prefix of `pattern[0..i]` that is also a
suffix of `pattern[0..i]`.

Example: pattern `ABABCABAB`

```text
index:  0 1 2 3 4 5 6 7 8
char:   A B A B C A B A B
pi:     0 0 1 2 0 1 2 3 4
```

- `pi[3] = 2` because `AB` is both a prefix and a suffix of `ABAB`.
- `pi[8] = 4` because `ABAB` is both a prefix and a suffix of `ABABCABAB`.

When a mismatch happens at pattern position `k`, the characters before `k` already match.
Instead of starting over, fall back to `k = pi[k-1]`, which is the longest prefix that
is also a suffix of the matched part.

## Code walkthrough — `kmp.py`

### `prefix_function(pattern)`

```python
k = 0
for i in range(1, m):
    while k > 0 and pattern[i] != pattern[k]:
        k = pi[k - 1]
    if pattern[i] == pattern[k]:
        k += 1
    pi[i] = k
```

- `k` is the length of the current matched prefix.
- On a mismatch, follow the fallback chain until a match or `k == 0`.
- If the next characters match, extend the prefix.
- `pi[i]` stores the best prefix length for the prefix ending at `i`.

The `while` loop is why the total preprocessing time is linear: `k` increases by at most
one per iteration and decreases along fallback links.

### `kmp_search(text, pattern)`

```python
k = 0
for i in range(n):
    while k > 0 and text[i] != pattern[k]:
        k = pi[k - 1]
    if text[i] == pattern[k]:
        k += 1
    if k == m:
        hits.append(i - m + 1)
        k = pi[k - 1]
```

- `k` is how many pattern characters currently match ending at `text[i]`.
- On mismatch, fall back in the pattern but keep the same text character.
- On a full match, record `i - m + 1`.
- Then set `k = pi[k - 1]` so overlapping matches are found.

The last step is the one people forget. For pattern `aa` in text `aaaa`, the correct
answer is `[0, 1, 2]`, not just `[0, 2]`.

### `kmp_count` and `kmp_first`

Thin wrappers over `kmp_search`: count occurrences, or return the first index / `-1`.

## Complexity

- Prefix function: `O(m)`.
- Search: `O(n)`.
- Total: `O(n + m)` time, `O(m)` extra space.

## Use cases

- Text editors and “find” features.
- Log scanning and intrusion detection.
- DNA and protein motif search.
- Searching patterns with repeated prefixes.
- Streaming search, where the text arrives in chunks.
- Counting overlapping occurrences.

## Common mistakes

- Thinking `pi[i]` includes the whole prefix. It must be a **proper** prefix.
- After a full match, resetting `k` to 0 and missing overlaps.
- Using `pattern[k]` when `k == m`; the full-match branch must run first.
- Mixing 0-indexed code with 1-indexed examples.
- Forgetting the empty-pattern case. In this implementation, an empty pattern matches at
  every position from `0` to `n`.

## Lab checklist

- [ ] Do you need all matches or only the first?
- [ ] Should overlapping matches count?
- [ ] Is the pattern empty?
- [ ] Are you returning start indices in the required indexing?
- [ ] Can you trace the prefix function for a short pattern?

---

# 5. Rabin-Karp

## What it solves

Rabin-Karp finds a pattern by hashing each window of the text and comparing hashes. It is
especially natural when you need to search for several patterns of the same length.

## Core idea

Treat a string as a number in base `b`:

```text
hash("ABC") = (A * b^2 + B * b + C) mod q
```

Compute the pattern hash and the first window hash. Then roll the window one character at
a time:

```text
new_hash = (b * (old_hash - outgoing * b^(m-1)) + incoming) mod q
```

If the window hash equals the pattern hash, verify the actual substring. The hash is only
a filter; collisions are possible.

## Code walkthrough — `rabin_karp.py`

### `rabin_karp(text, pattern, base=256, mod=1000000007)`

Initial hashes:

```python
high = pow(base, m - 1, mod)
hp = 0
ht = 0

for i in range(m):
    hp = (base * hp + ord(pattern[i])) % mod
    ht = (base * ht + ord(text[i])) % mod
```

- `base` is the polynomial base.
- `mod` is a large prime to keep numbers small.
- `high = base^(m-1) mod mod` is the weight of the outgoing character.
- `hp` is the pattern hash; `ht` is the current window hash.

Rolling:

```python
for s in range(n - m + 1):
    if hp == ht and text[s:s + m] == pattern:
        hits.append(s)
    if s < n - m:
        ht = (base * (ht - ord(text[s]) * high) + ord(text[s + m])) % mod
```

- Check the hash first.
- Only compare characters when the hashes match.
- Remove the outgoing character, shift the remaining hash left by multiplying by `base`,
  then add the incoming character.
- The final `% mod` keeps the hash in range.

### `rabin_karp_multi(text, patterns, ...)`

Builds a dictionary from hash to patterns:

```python
wanted.setdefault(h, []).append(p)
```

Then for each window, it looks up the window hash and verifies each candidate pattern.
All patterns must have the same length, because a single window length is used.

This is the version to use for:

- plagiarism detection,
- searching a dictionary of keywords,
- multiple DNA motifs of equal length.

## Complexity

- Preprocessing: `O(m)` for one pattern, or `O(total pattern length)` for several.
- Search: `O(n)` windows, each hash update `O(1)`.
- Verification: `O(m)` per hash hit.
- Average: `O(n + total pattern length)`.
- Worst: `O(nm)` if every window collides and verification scans the pattern each time.

## Use cases

- Multiple-pattern search.
- Plagiarism and document-similarity detection.
- DNA sequence search.
- Detecting duplicate substrings.
- Rolling-hash fingerprinting.
- Cases where hashing is simpler than building a KMP automaton.

## Common mistakes

- Skipping the character-by-character verification. A hash match is not a real match.
- Using a small modulus, which increases collisions.
- Forgetting `% mod` after subtraction; Python handles negative modulo, but other
  languages do not.
- Using different lengths in `rabin_karp_multi`.
- Forgetting that the rolling formula removes `text[s] * base^(m-1)`, not `text[s]`.

## Lab checklist

- [ ] One pattern or several?
- [ ] Are all patterns the same length?
- [ ] Did you verify every hash hit?
- [ ] Is the modulus large enough?
- [ ] Did you handle `m > n` and `m == 0`?

---

# Choosing the right algorithm

| Problem | Use | Why |
|---|---|---|
| Shortest path, unweighted | BFS | Fewest edges is the cost |
| Grid moves, nearest source | BFS | Layered expansion; multi-source works |
| Cycle, topological order, components | DFS | Ancestry and finish order matter |
| Shortest path, non-negative weights | Dijkstra | Greedy settling is correct |
| Shortest path, negative edges | Bellman-Ford | Dijkstra is invalid |
| One pattern, worst-case guarantee | KMP | `O(n + m)` deterministic |
| Many patterns, hash-friendly | Rabin-Karp | Rolling hash and multi-pattern lookup |
| Tiny text or baseline | Naïve | Simple and obviously correct |

# Lab workflow

1. Read the input format and output requirement.
2. Decide whether the graph is weighted.
3. Build the adjacency structure in 0-indexed form.
4. Choose the algorithm from the table above.
5. Write the core loop first, then add path reconstruction if needed.
6. Test on:
   - a single vertex,
   - a disconnected graph,
   - an unreachable target,
   - a cycle or a repeated pattern,
   - the smallest possible input.
7. State the complexity in the comments or final answer.

# Quick test cases

```python
# BFS
graph = [[1, 2], [0, 3], [0, 3], [1, 2, 4], [3]]
# dist = [0, 1, 1, 2, 3]
# path 0 -> 4 = [0, 1, 3, 4]

# DFS
# order = [0, 1, 3, 2, 4]

# Dijkstra
weighted = [
    [(1, 4), (2, 1)],
    [(0, 4), (2, 2), (3, 1)],
    [(0, 1), (1, 2), (3, 5)],
    [(1, 1), (2, 5)],
]
# dist = [0, 3, 1, 4]

# KMP / Rabin-Karp
text = "AABAACAADAABAABA"
pattern = "AABA"
# hits = [0, 9, 12]
```

# Final reminders

- BFS: mark on enqueue, not on pop.
- DFS: gray means “on the current recursion stack”; that is how you detect a directed
  cycle.
- Dijkstra: negative edges are a hard error, not a performance issue.
- KMP: after a full match, fall back with `k = pi[k - 1]` to keep overlaps.
- Rabin-Karp: always verify a hash hit.
- Write the complexity even when the question does not ask; it is usually worth marks.
