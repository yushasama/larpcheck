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

struct DSU {
  vi e;

  DSU(int n) : e(n, -1) {}
  
  int find(int x) {
    return e[x] < 0 ? x : e[x] = find(e[x]);
  }

  bool unite(int x, int y) {
    x = find(x), y = find(y);

    if (x == y) return false;

    if (e[x] > e[y]) swap(x, y);

    e[x] += e[y];
    e[y] = x;

    return true;
  }

  int size(int x) {
    return -e[find(x)];
  }
};

void solve() {
  int n, m;
  cin >> n >> m;

  ll b;
  cin >> b;

  vl c(n);
  rep(i, n) cin >> c[i];

  vector<vi> g(n);

  rep(i, m) {
    int u, v;
    cin >> u >> v;
    --u, --v;

    g[u].pb(v);
    g[v].pb(u);
  }

  DSU dsu(n);
  vb visited(n);

  rep(u, n) {
    for (auto& v : g[u]) dsu.unite(u, v);
  }

  vector<pair<ll, int>> a(n);
  rep(i, n) a[i] = {c[i], i};

  sort(all(a));

  ll res = -1;

  for (int i = 0; i < n; ++i) {
    int l = i + 1, r = n - 1;

    while (l < r) {
      ll s = a[i].first + a[l].first + a[r].first;

      if (s == b) {
        int u = a[i].second;
        int v = a[l].second;
        int w = a[r].second;

        set<int> cands;

        cands.insert(dsu.find(u));
        cands.insert(dsu.find(v));
        cands.insert(dsu.find(w));

        ll cand_sum = 0;

        for (auto& cand : cands) cand_sum += dsu.size(cand);

        res = max(res, cand_sum);

        ++l;
        --r;
      }

      else if (s < b) ++l;
      else --r;
    }
  }
 
  cout << res << "\n";
}

int main() {
  cin.tie(0);
  ios_base::sync_with_stdio(0);

  int t;
  cin >> t;

  rep(i,t) solve();
  return 0;
}