import math


def closest_pair(points):
    return _closest(sorted(points))


def _closest(px):
    n = len(px)
    if n <= 3:
        return _brute(px)

    mid = n // 2
    mid_x = px[mid][0]
    left = px[:mid]
    right = px[mid:]

    d = min(_closest(left), _closest(right))

    strip = [p for p in px if abs(p[0] - mid_x) < d]
    strip.sort(key=lambda p: p[1])

    for i in range(len(strip)):
        for j in range(i + 1, len(strip)):
            if strip[j][1] - strip[i][1] >= d:
                break
            d = min(d, _dist(strip[i], strip[j]))

    return d


def _brute(points):
    best = math.inf
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            best = min(best, _dist(points[i], points[j]))
    return best


def _dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


if __name__ == "__main__":
    points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    print(closest_pair(points))
