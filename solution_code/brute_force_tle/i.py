import itertools
import sys


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        cost = [[int(next(it)) for _ in range(n)] for _ in range(n)]
        best = 10**30
        for perm in itertools.permutations(range(n)):
            total = 0
            for i in range(n):
                total += cost[i][perm[i]]
            if total < best:
                best = total
        out.append(str(best))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
