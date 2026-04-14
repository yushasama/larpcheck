#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<vector<int>> cost(n, vector<int>(n));
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) cin >> cost[i][j];
        }

        vector<int> perm(n);
        iota(perm.begin(), perm.end(), 0);
        long long best = (long long)4e18;
        do {
            long long total = 0;
            for (int i = 0; i < n; ++i) total += cost[i][perm[i]];
            best = min(best, total);
        } while (next_permutation(perm.begin(), perm.end()));

        cout << best << '\n';
    }
}
