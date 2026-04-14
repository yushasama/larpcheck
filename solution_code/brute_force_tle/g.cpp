#include <bits/stdc++.h>
using namespace std;

struct Edge {
    int u;
    int v;
    long long w;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) {
        int n, m;
        long long B;
        cin >> n >> m >> B;
        vector<Edge> edges;
        for (int i = 0; i < m; ++i) {
            int u, v;
            long long w;
            cin >> u >> v >> w;
            --u;
            --v;
            edges.push_back({u, v, w});
            edges.push_back({v, u, w});
        }

        const long long INF = (long long)4e18;
        vector<long long> dist(n, INF);
        dist[0] = 0;
        for (int iter = 0; iter < n - 1; ++iter) {
            bool changed = false;
            for (const auto& e : edges) {
                if (dist[e.u] == INF) continue;
                if (dist[e.u] + e.w < dist[e.v]) {
                    dist[e.v] = dist[e.u] + e.w;
                    changed = true;
                }
            }
            if (!changed) break;
        }

        long long ans = dist[n - 1];
        if (ans == INF || ans > B) cout << -1 << '\n';
        else cout << ans << '\n';
    }
}
