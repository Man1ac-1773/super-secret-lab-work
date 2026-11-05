# Python algorithm templates

Standalone, exam-oriented templates. The new templates listed below contain plain
functions or one small class, use no imports, have no `if __name__ == "__main__"`,
and need no external dependencies.

## Conventions

- Vertices are `0 .. n-1`.
- Unweighted graphs: `graph[u]` is a list of neighbours.
- Weighted graphs: `graph[u]` is a list of `(v, weight)` pairs.
- Edge lists for Kruskal/Bellman-Ford: `(u, v, weight)`.
- `float("inf")` marks an unreachable vertex.
- Path helpers take the `parent` array returned by the search function.
- String indices are 0-based.

## Files

### Graphs and shortest paths

| File | Functions | Notes | Time |
|---|---|---|---|
| `bfs.py` | `bfs`, `bfs_path`, `multi_source_bfs`, `grid_bfs` | Queue BFS, unweighted shortest paths, multi-source, 4-direction grid | `O(V + E)` |
| `dfs.py` | `dfs`, `dfs_all`, `dfs_iterative` | Recursive DFS with colours/timestamps, all components, explicit stack | `O(V + E)` |
| `dijkstra.py` | `dijkstra`, `dijkstra_path`, `dijkstra_to_target` | Simple array implementation; non-negative weights only | `O(V^2)` |
| `dijkstra_heap.py` | `dijkstra_heap`, `dijkstra_heap_path` | Manual binary heap, no imports; use for large sparse graphs | `O((V + E) log V)` |
| `bellman_ford.py` | `bellman_ford`, `bellman_ford_path`, `bellman_ford_undirected` | Handles negative edges; returns `None` if a reachable negative cycle exists | `O(VE)` |
| `floyd_warshall.py` | `floyd_warshall`, `floyd_warshall_paths`, `has_negative_cycle`, `rebuild_path` | All-pairs shortest paths and path reconstruction | `O(V^3)` |
| `topological_sort.py` | `topological_sort`, `topological_sort_dfs` | Kahn's algorithm and DFS version; returns `[]` on a cycle | `O(V + E)` |
| `cycle_detection.py` | `has_cycle_undirected`, `has_cycle_directed` | Parent check for undirected, three-colour DFS for directed | `O(V + E)` |
| `connected_components.py` | `connected_components` | Returns a list of component lists | `O(V + E)` |
| `bipartite.py` | `is_bipartite` | BFS two-colouring | `O(V + E)` |
| `disjoint_set.py` | `DSU` | Path halving and union by size | `O(alpha(n))` amortised |
| `kruskal.py` | `kruskal` | Returns `(total_weight, chosen_edges)` | `O(E log E)` |
| `prim.py` | `prim` | Array version, returns `(total_weight, chosen_edges)` | `O(V^2)` |
| `warshall.py` | `transitive_closure` | Boolean reachability matrix | `O(V^3)` |

### String matching

| File | Functions | Notes | Time |
|---|---|---|---|
| `naive_string_match.py` | `naive_search` | Reference implementation | `O((n-m+1)m)` |
| `kmp.py` | `prefix_function`, `kmp_search`, `kmp_count`, `kmp_first` | Prefix function and overlap-aware search | `O(n + m)` |
| `rabin_karp.py` | `rabin_karp`, `rabin_karp_multi` | Rolling hash; verifies candidates to avoid false positives | `O(n + m)` average |
| `finite_automaton.py` | `prefix_function`, `build_automaton`, `automaton_search` | KMP automaton over an explicit alphabet | `O(n + m * alphabet_size)` |
| `boyer_moore.py` | `boyer_moore` | Bad-character and good-suffix rules | `O(nm)` worst, sublinear in practice |

## Quick usage

```python
from bfs import bfs, bfs_path
from dijkstra import dijkstra
from kmp import kmp_search

graph = [[1, 2], [0, 3], [0, 3], [1, 2, 4], [3]]

dist, parent, order = bfs(graph, 0)
path = bfs_path(parent, 0, 4)          # [0, 1, 3, 4]

weighted = [[(1, 4), (2, 1)], [(0, 4), (2, 2), (3, 1)], [(0, 1), (1, 2), (3, 5)], [(1, 1), (2, 5)]]
dist, parent = dijkstra(weighted, 0)   # [0, 3, 1, 4]

hits = kmp_search("AABAACAADAABAABA", "AABA")  # [0, 9, 12]
```

## Exam notes

- `dijkstra.py` is deliberately the simplest version. Switch to `dijkstra_heap.py` when
  `V` is large and the graph is sparse.
- Dijkstra fails on negative edges; use Bellman-Ford.
- `bfs` returns distances only for the connected component of `start`; use
  `multi_source_bfs` or `dfs_all` for disconnected graphs.
- `kruskal` and `prim` return the total MST weight and the chosen edges, so either can
  be printed directly.
- `rabin_karp_multi` requires all patterns to have the same length.
- `finite_automaton.py` builds the alphabet from the text and pattern when `alphabet`
  is omitted.
