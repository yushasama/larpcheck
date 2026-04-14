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
        target = int(next(it))
        arr = [int(next(it)) for _ in range(n)]
        for i in range(n):
            found = False
            for j in range(i + 1, n):
                if arr[i] + arr[j] == target:
                    out.append(f"{i} {j}")
                    found = True
                    break
            if found:
                break
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
