#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct Edge {
    int to;
    ll w;
};

const ll INF = (ll)4e18;

int n, m;
ll B;
vector<vector<Edge>> g;
vector<int> vis;
ll ans;

void dfs(int u, ll cost) {
    if (cost > B) return;
    if (cost >= ans) return;

    if (u == n - 1) {
        ans = min(ans, cost);
        return;
    }

    vis[u] = 1;

    for (auto &e : g[u]) {
        if (!vis[e.to]) {
            dfs(e.to, cost + e.w);
        }
    }

    vis[u] = 0;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) {
        cin >> n >> m >> B;

        g.assign(n, {});
        for (int i = 0; i < m; i++) {
            int u, v;
            ll w;
            cin >> u >> v >> w;
            --u; --v;

            g[u].push_back({v, w});
            g[v].push_back({u, w});
        }

        vis.assign(n, 0);
        ans = INF;

        dfs(0, 0);

        if (ans == INF || ans > B) cout << -1 << '\n';
        else cout << ans << '\n';
    }
}