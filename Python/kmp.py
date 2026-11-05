def prefix_function(pattern):
    """pi[i] = longest proper prefix of pattern[0..i] that is also a suffix."""
    m = len(pattern)
    pi = [0] * m
    k = 0

    for i in range(1, m):
        while k > 0 and pattern[i] != pattern[k]:
            k = pi[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        pi[i] = k

    return pi


def kmp_search(text, pattern):
    """Return all starting indices of pattern in text, including overlaps."""
    n = len(text)
    m = len(pattern)

    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []

    pi = prefix_function(pattern)
    hits = []
    k = 0

    for i in range(n):
        while k > 0 and text[i] != pattern[k]:
            k = pi[k - 1]
        if text[i] == pattern[k]:
            k += 1
        if k == m:
            hits.append(i - m + 1)
            k = pi[k - 1]

    return hits


def kmp_count(text, pattern):
    """Number of occurrences, including overlaps."""
    return len(kmp_search(text, pattern))


def kmp_first(text, pattern):
    """First starting index, or -1."""
    hits = kmp_search(text, pattern)
    if hits:
        return hits[0]
    return -1
