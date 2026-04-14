#include <bits/stdc++.h>
using namespace std;

bool is_palindrome(const vector<int>& a, int l, int r) {
    while (l < r) {
        if (a[l] != a[r]) return false;
        ++l;
        --r;
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int> a(n);
        for (int i = 0; i < n; ++i) cin >> a[i];

        vector<vector<int>> dp(n, vector<int>(n, n + 1));
        for (int i = 0; i < n; ++i) dp[i][i] = 1;

        for (int len = 2; len <= n; ++len) {
            for (int l = 0; l + len <= n; ++l) {
                int r = l + len - 1;
                if (is_palindrome(a, l, r)) dp[l][r] = 1;
                for (int k = l; k < r; ++k) {
                    dp[l][r] = min(dp[l][r], dp[l][k] + dp[k + 1][r]);
                }
            }
        }

        cout << dp[0][n - 1] << '\n';
    }
}
