def quicksort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low >= high:
        return arr
    pivot = partition(arr, low, high)
    quicksort(arr, low, pivot - 1)
    quicksort(arr, pivot + 1, high)
    return arr


def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


if __name__ == "__main__":
    data = [10, 7, 8, 9, 1, 5]
    print(quicksort(data))
