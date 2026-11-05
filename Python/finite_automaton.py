def prefix_function(pattern):
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


def build_automaton(pattern, alphabet):
    """Transition table delta[state][char_index] for KMP's automaton."""
    m = len(pattern)
    pi = prefix_function(pattern)
    delta = [[0] * len(alphabet) for _ in range(m + 1)]

    for state in range(m + 1):
        for index in range(len(alphabet)):
            ch = alphabet[index]
            if state < m and ch == pattern[state]:
                delta[state][index] = state + 1
            elif state == 0:
                delta[state][index] = 0
            else:
                delta[state][index] = delta[pi[state - 1]][index]

    return delta


def automaton_search(text, pattern, alphabet=None):
    """Finite-automaton string matching. Returns all starting indices."""
    n = len(text)
    m = len(pattern)

    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []

    if alphabet is None:
        alphabet = sorted(set(text + pattern))

    index = {ch: i for i, ch in enumerate(alphabet)}
    delta = build_automaton(pattern, alphabet)

    state = 0
    hits = []

    for i in range(n):
        ch = text[i]
        if ch not in index:
            state = 0
            continue
        state = delta[state][index[ch]]
        if state == m:
            hits.append(i - m + 1)
            state = delta[state][index[ch]]

    return hits
