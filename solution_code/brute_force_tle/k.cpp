#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) {
        int n, target;
        cin >> n >> target;
        vector<long long> a(n);
        for (int i = 0; i < n; ++i) cin >> a[i];
        for (int i = 0; i < n; ++i) {
            bool done = false;
            for (int j = i + 1; j < n; ++j) {
                if (a[i] + a[j] == target) {
                    cout << i << ' ' << j << '\n';
                    done = true;
                    break;
                }
            }
            if (done) break;
        }
    }
}
