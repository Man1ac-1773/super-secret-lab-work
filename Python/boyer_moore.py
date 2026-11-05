def _good_suffix(pattern):
    """Good-suffix shift table. shift[j] is used for a mismatch at j-1."""
    m = len(pattern)
    shift = [0] * (m + 1)
    border = [0] * (m + 1)

    i = m
    j = m + 1
    border[i] = j

    while i > 0:
        while j <= m and pattern[i - 1] != pattern[j - 1]:
            if shift[j] == 0:
                shift[j] = j - i
            j = border[j]
        i -= 1
        j -= 1
        border[i] = j

    j = border[0]
    for i in range(m + 1):
        if shift[i] == 0:
            shift[i] = j
        if i == j:
            j = border[j]

    return shift


def boyer_moore(text, pattern):
    """Boyer-Moore with bad-character and good-suffix rules."""
    n = len(text)
    m = len(pattern)

    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []

    last = {}
    for i in range(m):
        last[pattern[i]] = i

    shift = _good_suffix(pattern)
    hits = []
    s = 0

    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            hits.append(s)
            s += shift[0]
        else:
            bad = j - last.get(text[s + j], -1)
            s += max(1, bad, shift[j + 1])

    return hits
