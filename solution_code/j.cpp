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

struct Reroot {
  vl down;
  vl haul;
  vl sub_r;
  vl vals;
  vector<vi> g;
  int n;
  ll total_r = 0;

  Reroot(int n, const vector<vi>& g, const vl& vals) : n(n), haul(n), sub_r(n), down(n), g(g), vals(vals) {}

  void dfs1(int u, int p) {
    sub_r[u] = vals[u];
    down[u] = 0;

    for (auto& v : g[u]) {
      if (v == p) continue;
      dfs1(v, u);

      sub_r[u] += sub_r[v];
      down[u] += down[v] + sub_r[v];
    }
  }

  void dfs2(int u, int p, ll cur_down) {
    haul[u] = n * total_r - cur_down;

    for (auto& v : g[u]) {
      if (v == p) continue;

      ll new_down = cur_down + total_r - 2 * sub_r[v];

      dfs2(v, u, new_down);
    }
  }

  void build(int root) {
    dfs1(root, -1);
    total_r = sub_r[root];

    dfs2(root, -1, down[root]);
  }
};

void solve() {
  int n;
  cin >> n;

  vl a(n);
  rep(i, n) cin >> a[i];

  vector<vi> g(n);

  rep(i, n-1) {
    int u, v;
    cin >> u >> v;
    
    --u, --v;

    g[u].pb(v);
    g[v].pb(u);
  }

  Reroot rrt(n, g, a);
  rrt.build(0);

  rep(i, n) cout << rrt.haul[i] << " \n"[i == n-1];
}

int main() {
  cin.tie(0);
  ios_base::sync_with_stdio(0);

  int t;
  cin >> t;

  rep(i,t) solve();
  return 0;
}