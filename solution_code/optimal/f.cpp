#include <bits/stdc++.h>
using namespace std;

#define rep(i,n) for (int i=0; i < (n); ++i)
#define rrep(i,n) for (int i=1; i <= (n); ++i)
#define drep(i,n) for (int i=(n)-1; i >= 0; --i)
#define drrep(i,n) for (int i = (n); i >= 0; --i)
#define all(a) (a).begin(), (a).end()

#define ll long long
#define db double
#define pii pair<int, int>
#define pll pair<ll, ll>
#define pdb pair<db, db>
#define vi vector<int>
#define vl vector<ll>
#define vc vector<char>
#define vdb vector<db>
#define vb vector<bool>

#define pb push_back
#define sz(x) (int)(x).size()
#define maxs(x,y) (x = max(x,y))
#define mins(x,y) (x = min(x,y))
#define popcnt(x) (__builtin_popcount(x))

#define yn(a) ((a) ? "YES" : "NO")
#define fs(a) ((a) ? "FIRST" : "SECOND")

const int MOD = 1000000007;
const int INF = 1000000000;
const ll LINF = 1000000000000000000LL;
const double EPS = 1e-10;

void solve() {
  int n;
  cin >> n;

  vector<set<int>> g(n);

  rep(u, n) {
    int v;
    cin >> v;

    --v;

    g[u].insert(v);
    g[v].insert(u);
  }

  vb visited(n);

  int c, b;
  c = b = 0;

  rep(i, n) {
    if (visited[i]) continue;
    visited[i] = true;

    queue<int> q;
    q.push(i);

    bool is_cycle = true;

    while (!q.empty()) {
      int u = q.front();
      q.pop();

      visited[u] = true;

      if (sz(g[u]) != 2) is_cycle = false;

      for (auto& v : g[u]) {
        if (visited[v]) continue;
        q.push(v);
      }
    }

    if (is_cycle) ++c;
    else ++b;
  }

  cout << c + min(1, b) << " " << c + b << "\n";
}

int main() {
  cin.tie(0);
  ios_base::sync_with_stdio(0);

  int t;
  cin >> t;

  rep(i,t) solve();
  return 0;
}