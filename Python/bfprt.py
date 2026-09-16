def bfprt(arr, k):
    if k < 0 or k >= len(arr):
        raise IndexError("k out of range")
    return select(arr, k)


def select(arr, k):
    if len(arr) <= 5:
        return sorted(arr)[k]

    groups = [arr[i:i + 5] for i in range(0, len(arr), 5)]
    medians = [sorted(g)[len(g) // 2] for g in groups]
    pivot = select(medians, len(medians) // 2)

    left = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    if k < len(left):
        return select(left, k)
    if k < len(left) + len(equal):
        return pivot
    return select(right, k - len(left) - len(equal))


if __name__ == "__main__":
    data = [12, 3, 5, 7, 4, 19, 26, 1, 2, 8]
    k = 3
    print(bfprt(data, k))
