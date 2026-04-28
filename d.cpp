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
  vl euler;
  vi tin, tout;
  int timer = 0;

  Euler(int n) : euler(n), tin(n), tout(n) {}

  void dfs(int u, int p, vector<vi>& g, vl& val) {
    tin[u] = timer;
    euler[timer] = val[u];
    ++timer;

    for (auto& v : g[u]) {
      if (v == p) continue;
      dfs(v, u, g, val);
    }

    tout[u] = timer - 1;
  }

  void build(int root, vector<vi>& g,  vl& val) {
    dfs(root, -1, g, val);
  }
};

void solve() {
  int n, q;
  cin >> n >> q;

  vl a(n);
  rep(i, n) cin >> a[i];

  vector<vi> g(n);

  rep(i, m) {
    int u, v;
    cin >> u >> v;

    --u, --v;

    g[u].pb(v);
    g[v].pb(u);
  }

  Euler et(n, g, a);
  et.build(0, g, a);

  while (q--) {
    int u;
    cin >> u;
    
    --u;

    cout <<
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