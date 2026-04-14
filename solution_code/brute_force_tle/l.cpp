#include <bits/stdc++.h>
using namespace std;

int bfs_reach(const vector<vector<int>>& g, const vector<int>& starts) {
    vector<int> vis((int)g.size(), 0);
    queue<int> q;
    for (int s : starts) {
        if (!vis[s]) {
            vis[s] = 1;
            q.push(s);
        }
    }
    int count = 0;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        ++count;
        for (int v : g[u]) {
            if (!vis[v]) {
                vis[v] = 1;
                q.push(v);
            }
        }
    }
    return count;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) {
        int n, m;
        long long B;
        cin >> n >> m >> B;
        vector<long long> fee(n);
        for (int i = 0; i < n; ++i) cin >> fee[i];
        vector<vector<int>> g(n);
        for (int i = 0; i < m; ++i) {
            int u, v;
            cin >> u >> v;
            --u;
            --v;
            g[u].push_back(v);
            g[v].push_back(u);
        }

        int best = -1;
        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {
                for (int k = j + 1; k < n; ++k) {
                    if (fee[i] + fee[j] + fee[k] != B) continue;
                    best = max(best, bfs_reach(g, {i, j, k}));
                }
            }
        }
        cout << best << '\n';
    }
}
