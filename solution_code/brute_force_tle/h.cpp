#include <bits/stdc++.h>
using namespace std;

long long subtree_sum(int u, int parent, const vector<vector<int>>& g, const vector<long long>& vals) {
    long long total = vals[u];
    for (int v : g[u]) {
        if (v == parent) continue;
        total += subtree_sum(v, u, g, vals);
    }
    return total;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) {
        int n, q;
        cin >> n >> q;
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

        vector<int> parent(n, -1);
        queue<int> qu;
        qu.push(0);
        parent[0] = 0;
        while (!qu.empty()) {
            int u = qu.front();
            qu.pop();
            for (int v : g[u]) {
                if (parent[v] != -1) continue;
                parent[v] = u;
                qu.push(v);
            }
        }

        while (q--) {
            int type, u;
            cin >> type >> u;
            --u;
            if (type == 1) {
                long long x;
                cin >> x;
                vals[u] = x;
            } else {
                cout << subtree_sum(u, parent[u], g, vals) << '\n';
            }
        }
    }
}
