import sys
from collections import deque


def bfs_reach(graph: list[list[int]], starts: tuple[int, int, int]) -> int:
    seen = [False] * len(graph)
    dq = deque()
    for s in starts:
        if not seen[s]:
            seen[s] = True
            dq.append(s)
    count = 0
    while dq:
        u = dq.popleft()
        count += 1
        for v in graph[u]:
            if not seen[v]:
                seen[v] = True
                dq.append(v)
    return count


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        m = int(next(it))
        budget = int(next(it))
        fee = [int(next(it)) for _ in range(n)]
        graph = [[] for _ in range(n)]
        for _ in range(m):
            u = int(next(it)) - 1
            v = int(next(it)) - 1
            graph[u].append(v)
            graph[v].append(u)

        best = -1
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if fee[i] + fee[j] + fee[k] != budget:
                        continue
                    best = max(best, bfs_reach(graph, (i, j, k)))
        out.append(str(best))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
