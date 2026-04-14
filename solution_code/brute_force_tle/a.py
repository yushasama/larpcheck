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
        for i in range(1, n + 1):
            div3 = False
            div5 = False
            for x in range(3, i + 1, 3):
                if x == i:
                    div3 = True
            for x in range(5, i + 1, 5):
                if x == i:
                    div5 = True
            if div3 and div5:
                out.append("UmaMusume")
            elif div3:
                out.append("Uma")
            elif div5:
                out.append("Musume")
            else:
                out.append(str(i))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
