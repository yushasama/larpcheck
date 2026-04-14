#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) {
        int n, q;
        cin >> n >> q;
        vector<long long> a(n);
        for (int i = 0; i < n; ++i) cin >> a[i];
        while (q--) {
            int r;
            cin >> r;
            long long sum = 0;
            for (int i = 0; i < r; ++i) sum += a[i];
            cout << sum << '\n';
        }
    }
}
