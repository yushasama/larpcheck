import sys
from collections import deque


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        vals = [int(next(it)) for _ in range(n)]
        graph = [[] for _ in range(n)]
        for _ in range(n - 1):
            u = int(next(it)) - 1
            v = int(next(it)) - 1
            graph[u].append(v)
            graph[v].append(u)

        answer = []
        for start in range(n):
            dist = [-1] * n
            dq = deque([start])
            dist[start] = 0
            while dq:
                u = dq.popleft()
                for v in graph[u]:
                    if dist[v] != -1:
                        continue
                    dist[v] = dist[u] + 1
                    dq.append(v)

            total = 0
            for v in range(n):
                total += vals[v] * (n - dist[v])
            answer.append(str(total))
        out.append(" ".join(answer))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
