import sys


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    t = int(next(it))
    out = []
    inf = 10**30
    for _ in range(t):
        n = int(next(it))
        m = int(next(it))
        budget = int(next(it))
        edges = []
        for _ in range(m):
            u = int(next(it)) - 1
            v = int(next(it)) - 1
            w = int(next(it))
            edges.append((u, v, w))
            edges.append((v, u, w))

        dist = [inf] * n
        dist[0] = 0
        for _ in range(n - 1):
            changed = False
            for u, v, w in edges:
                if dist[u] == inf:
                    continue
                nd = dist[u] + w
                if nd < dist[v]:
                    dist[v] = nd
                    changed = True
            if not changed:
                break

        ans = dist[-1]
        out.append(str(-1 if ans == inf or ans > budget else ans))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
