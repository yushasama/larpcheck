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
        remember = [int(next(it)) - 1 for _ in range(n)]
        graph = [[] for _ in range(n)]
        for i, v in enumerate(remember):
            graph[i].append(v)
            graph[v].append(i)

        used = [False] * n
        cycles = 0
        other = 0
        for start in range(n):
            if used[start]:
                continue
            dq = deque([start])
            used[start] = True
            nodes = []
            while dq:
                u = dq.popleft()
                nodes.append(u)
                for v in range(n):
                    adjacent = False
                    for to in graph[u]:
                        if to == v:
                            adjacent = True
                            break
                    if adjacent and not used[v]:
                        used[v] = True
                        dq.append(v)

            is_cycle = True
            for u in nodes:
                if len(set(graph[u])) != 2:
                    is_cycle = False
            if is_cycle:
                cycles += 1
            else:
                other += 1

        out.append(f"{cycles + min(1, other)} {cycles + other}")
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
