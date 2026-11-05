def naive_search(text, pattern):
    """Brute-force string matching; returns all starting indices."""
    n = len(text)
    m = len(pattern)

    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []

    hits = []
    for s in range(n - m + 1):
        j = 0
        while j < m and text[s + j] == pattern[j]:
            j += 1
        if j == m:
            hits.append(s)

    return hits
