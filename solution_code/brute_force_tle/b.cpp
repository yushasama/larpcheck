#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) {
        int n, k;
        cin >> n >> k;
        vector<int> a(n);
        for (int i = 0; i < n; ++i) cin >> a[i];
        int answer = -1;
        for (int i = 0; i < n; ++i) {
            if (a[i] == k) {
                answer = i;
                break;
            }
        }
        cout << answer << '\n';
    }
}
