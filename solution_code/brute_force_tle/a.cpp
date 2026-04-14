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
        for (int i = 1; i <= n; ++i) {
            bool div3 = false;
            bool div5 = false;
            for (int x = 3; x <= i; x += 3) {
                if (x == i) div3 = true;
            }
            for (int x = 5; x <= i; x += 5) {
                if (x == i) div5 = true;
            }
            if (div3 && div5) cout << "UmaMusume\n";
            else if (div3) cout << "Uma\n";
            else if (div5) cout << "Musume\n";
            else cout << i << '\n';
        }
    }
}
