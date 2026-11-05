def transitive_closure(matrix):
    """Boolean transitive closure of a directed graph.

    matrix[i][j] is True if there is an edge i -> j.
    Returns a new matrix where reach[i][j] is True if j is reachable from i.
    """
    n = len(matrix)
    reach = [[bool(matrix[i][j]) for j in range(n)] for i in range(n)]

    for i in range(n):
        reach[i][i] = True

    for k in range(n):
        for i in range(n):
            if not reach[i][k]:
                continue
            for j in range(n):
                if reach[k][j]:
                    reach[i][j] = True

    return reach
