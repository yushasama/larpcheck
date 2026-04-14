import sys


def is_palindrome(arr: list[int], left: int, right: int) -> bool:
    while left < right:
        if arr[left] != arr[right]:
            return False
        left += 1
        right -= 1
    return True


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        arr = [int(next(it)) for _ in range(n)]
        dp = [[n + 1] * n for _ in range(n)]
        for i in range(n):
            dp[i][i] = 1
        for length in range(2, n + 1):
            for left in range(0, n - length + 1):
                right = left + length - 1
                if is_palindrome(arr, left, right):
                    dp[left][right] = 1
                for mid in range(left, right):
                    cand = dp[left][mid] + dp[mid + 1][right]
                    if cand < dp[left][right]:
                        dp[left][right] = cand
        out.append(str(dp[0][n - 1]))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
