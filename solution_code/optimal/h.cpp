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

struct Euler {
  vl tour;
  vi tin;
  vi tout;
  vector<vi> g;
  vl vals;
  int timer = 0;

  Euler(int n, const vector<vi>& g, const vl& vals) : tour(n), tin(n), tout(n), g(g), vals(vals) {}

  void dfs(int u, int p) {
    tin[u] = timer;
    tour[timer] = vals[u];
    ++timer;

    for (auto& v : g[u]) {
      if (v == p) continue;
      dfs(v, u);
    }

    tout[u] = timer - 1;
  }

  void build(int root) {
    dfs(root, -1);
  }
};

struct Fenwick {
  vl bit;
  int n;

  Fenwick(int n) : n(n), bit(n+1) {}

  void add(int i, ll x) {
    for (; i <= n; i += i & -i) bit[i] += x;
  }

  void update(int i, ll x) {
    ll cur = sum(i) - sum(i-1);
    ll delta = x - cur;

    add(i, delta);
  }

  ll sum (int i) {
    ll s = 0;

    for (; i > 0; i -= i & -i) s += bit[i];
    return s;
  }

  ll query(int l, int r) {
    return sum(r) - sum(l-1);
  }
};

void solve() {
  int n, q;
  cin >> n >> q;

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

  Euler et(n, g, a);
  et.build(0);

  Fenwick ft(n);

  rep(i, n) ft.add(i+1, et.tour[i]);

  while (q--) {
    int t, u;
    ll x;

    cin >> t >> u;

    --u;

    if (t == 1) {
      cin >> x;

      ft.update(et.tin[u] + 1, x);
    }

    else cout << ft.query(et.tin[u] + 1, et.tout[u] + 1) << "\n";
  }
}

int main() {
  cin.tie(0);
  ios_base::sync_with_stdio(0);

  int t;
  cin >> t;

  rep(i,t) solve();
  return 0;
}