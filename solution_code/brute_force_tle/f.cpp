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
        vector<int> remember(n);
        for (int i = 0; i < n; ++i) {
            cin >> remember[i];
            --remember[i];
        }

        vector<vector<int>> g(n);
        for (int i = 0; i < n; ++i) {
            g[i].push_back(remember[i]);
            g[remember[i]].push_back(i);
        }

        vector<int> used(n, 0);
        int cycles = 0;
        int other = 0;
        for (int start = 0; start < n; ++start) {
            if (used[start]) continue;
            queue<int> q;
            q.push(start);
            used[start] = 1;
            vector<int> nodes;
            while (!q.empty()) {
                int u = q.front();
                q.pop();
                nodes.push_back(u);
                for (int v = 0; v < n; ++v) {
                    bool adjacent = false;
                    for (int to : g[u]) {
                        if (to == v) {
                            adjacent = true;
                            break;
                        }
                    }
                    if (adjacent && !used[v]) {
                        used[v] = 1;
                        q.push(v);
                    }
                }
            }

            bool is_cycle = true;
            for (int u : nodes) {
                set<int> uniq(g[u].begin(), g[u].end());
                if ((int)uniq.size() != 2) is_cycle = false;
            }
            if (is_cycle) ++cycles;
            else ++other;
        }
        cout << cycles + min(1, other) << ' ' << cycles + other << '\n';
    }
}
