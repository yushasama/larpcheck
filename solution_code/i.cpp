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

  vector<vi> e(n, vi(n));

  rep(i, n) rep(j, n) cin >> e[i][j];

  int N = 1 << n;

  vi dp(N, INF);
  dp[0] = 0;

  for (int mask = 0; mask < N; ++mask) {
    int i = popcnt(mask);

    for (int j = 0; j < n; ++j) {
      if (!(mask & (1 << j))) {
        int nmask = mask | (1 << j);

        dp[nmask] = min(dp[nmask], dp[mask] + e[i][j]);
      }
    }
  }

  cout << dp[N-1] << "\n";
}

int main() {
  cin.tie(0);
  ios_base::sync_with_stdio(0);

  int t;
  cin >> t;

  rep(i,t) solve();
  return 0;
}