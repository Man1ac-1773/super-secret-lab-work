def rabin_karp(text, pattern, base=256, mod=1000000007):
    """Return all starting indices of pattern in text using rolling hashes."""
    n = len(text)
    m = len(pattern)

    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []

    high = pow(base, m - 1, mod)
    hp = 0
    ht = 0

    for i in range(m):
        hp = (base * hp + ord(pattern[i])) % mod
        ht = (base * ht + ord(text[i])) % mod

    hits = []

    for s in range(n - m + 1):
        if hp == ht and text[s:s + m] == pattern:
            hits.append(s)
        if s < n - m:
            ht = (base * (ht - ord(text[s]) * high) + ord(text[s + m])) % mod

    return hits


def rabin_karp_multi(text, patterns, base=256, mod=1000000007):
    """Find several patterns of the same length; returns {pattern: [indices]}."""
    result = {p: [] for p in patterns}
    if not patterns:
        return result

    m = len(patterns[0])
    if any(len(p) != m for p in patterns):
        raise ValueError("all patterns must have the same length")
    if m == 0:
        indices = list(range(len(text) + 1))
        for p in patterns:
            result[p] = indices[:]
        return result
    if m > len(text):
        return result

    high = pow(base, m - 1, mod)
    wanted = {}
    for p in patterns:
        h = 0
        for ch in p:
            h = (base * h + ord(ch)) % mod
        wanted.setdefault(h, []).append(p)

    ht = 0
    for i in range(m):
        ht = (base * ht + ord(text[i])) % mod

    for s in range(len(text) - m + 1):
        if ht in wanted:
            window = text[s:s + m]
            for p in set(wanted[ht]):
                if window == p:
                    result[p].append(s)
        if s < len(text) - m:
            ht = (base * (ht - ord(text[s]) * high) + ord(text[s + m])) % mod

    return result
