import sys


def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        k = int(next(it))
        arr = [int(next(it)) for _ in range(n)]
        ans = -1
        for i, value in enumerate(arr):
            if value == k:
                ans = i
                break
        out.append(str(ans))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
