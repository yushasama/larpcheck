import sys
from collections import deque

sys.setrecursionlimit(1_000_000)


def subtree_sum(u: int, parent: int, graph: list[list[int]], vals: list[int]) -> int:
    total = vals[u]
    for v in graph[u]:
        if v == parent:
            continue
        total += subtree_sum(v, u, graph, vals)
    return total


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        q = int(next(it))
        vals = [int(next(it)) for _ in range(n)]
        graph = [[] for _ in range(n)]
        for _ in range(n - 1):
            u = int(next(it)) - 1
            v = int(next(it)) - 1
            graph[u].append(v)
            graph[v].append(u)

        parent = [-1] * n
        dq = deque([0])
        parent[0] = 0
        while dq:
            u = dq.popleft()
            for v in graph[u]:
                if parent[v] != -1:
                    continue
                parent[v] = u
                dq.append(v)

        for _ in range(q):
            u = int(next(it)) - 1
            out.append(str(subtree_sum(u, parent[u], graph, vals)))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
