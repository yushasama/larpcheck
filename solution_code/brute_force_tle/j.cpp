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
        vector<long long> vals(n);
        for (int i = 0; i < n; ++i) cin >> vals[i];
        vector<vector<int>> g(n);
        for (int i = 0; i < n - 1; ++i) {
            int u, v;
            cin >> u >> v;
            --u;
            --v;
            g[u].push_back(v);
            g[v].push_back(u);
        }

        vector<long long> ans(n, 0);
        for (int start = 0; start < n; ++start) {
            vector<int> dist(n, -1);
            queue<int> q;
            q.push(start);
            dist[start] = 0;
            while (!q.empty()) {
                int u = q.front();
                q.pop();
                for (int v : g[u]) {
                    if (dist[v] != -1) continue;
                    dist[v] = dist[u] + 1;
                    q.push(v);
                }
            }
            long long total = 0;
            for (int v = 0; v < n; ++v) {
                total += vals[v] * 1LL * (n - dist[v]);
            }
            ans[start] = total;
        }

        for (int i = 0; i < n; ++i) {
            cout << ans[i] << (i + 1 == n ? '\n' : ' ');
        }
    }
}
