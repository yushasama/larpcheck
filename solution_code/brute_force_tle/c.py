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
        q = int(next(it))
        arr = [int(next(it)) for _ in range(n)]
        for _ in range(q):
            r = int(next(it))
            total = 0
            for i in range(r):
                total += arr[i]
            out.append(str(total))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
