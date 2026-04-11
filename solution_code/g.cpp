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

#define yn(a) ((a) ? "Yes" : "No")
#define fs(a) ((a) ? "First" : "Second")

const int MOD = 1000000007;
const int INF = 1000000000;
const ll LINF = 1000000000000000000LL;
const double EPS = 1e-10;

int main() {
  cin.tie(0);
  ios_base::sync_with_stdio(0);

  int n, m;
  ll b;

  cin >> n >> m >> b;

  vector<iii> g(n);

  rep(i, m) {
    int u, v;
    ll c;

    cin >> u >> v >> c;

    --u, --v;

    g[u].pb({v, c});
    g[v].pb({u, c});
  }

  vl dist(n, LINF);
  priority_queue<pair<ll, int>, vector<pair<ll, int>, greater<>> pq;
  
  dist[0] = 0;
  pq.push({0, 0});

  while (!pq.empty()) {
    auto [d, u] = pq.top();
    pq.pop();

    if (d > dist[u]) continue;

    for (auto [v, c] : g[u]) {
      ll nd = dist[u] + c;

      if (nd < dist[v]) {
        dist[v] = nd;
        pq.push({nd, v});
      }
    }
  }

  ll res = dist[n-1];

  cout << (res == LINF || res > b > -1 : res) << "\n";

  return 0;
}