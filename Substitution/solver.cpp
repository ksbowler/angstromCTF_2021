#include <bits/stdc++.h>
using namespace std;

struct ModIntR {
  int x;
  ModIntR() : x(0) {}
  ModIntR(int64_t y)
      : x(y >= 0 ? y % mod()
                 : (mod() - (-y) % mod()) % mod()) {}
  static int &mod() {
    static int mod = 0;
    return mod;
  }
  static void set_mod(int md) { mod() = md; }
  ModIntR &operator+=(const ModIntR &p) {
    if((x += p.x) >= mod()) x -= mod();
    return *this;
  }
  ModIntR &operator-=(const ModIntR &p) {
    if((x += mod() - p.x) >= mod()) x -= mod();
    return *this;
  }

  ModIntR &operator*=(const ModIntR &p) {
    long long m = mod();
    x = (int)(1LL * x * p.x % m);
    return *this;
  }

  ModIntR &operator/=(const ModIntR &p) {
    *this *= p.inverse();
    return *this;
  }

  ModIntR operator-() const { return ModIntR(-x); }

  ModIntR operator+(const ModIntR &p) const {
    return ModIntR(*this) += p;
  }

  ModIntR operator-(const ModIntR &p) const {
    return ModIntR(*this) -= p;
  }

  ModIntR operator*(const ModIntR &p) const {
    return ModIntR(*this) *= p;
  }

  ModIntR operator/(const ModIntR &p) const {
    return ModIntR(*this) /= p;
  }

  bool operator==(const ModIntR &p) const {
    return x == p.x;
  }

  bool operator!=(const ModIntR &p) const {
    return x != p.x;
  }

  ModIntR inverse() const {
    int a = x, b = mod(), u = 1, v = 0, t;
    while(b > 0) {
      t = a / b;
      swap(a -= t * b, b);
      swap(u -= t * v, v);
    }
    return ModIntR(u);
  }

  ModIntR pow(int64_t n) const {
    ModIntR res(1), mul(x);
    while(n) {
      if(n & 1) res *= mul;
      mul *= mul;
      n >>= 1;
    }
    return res;
  }

  friend ostream &operator<<(ostream &os,
                             const ModIntR &p) {
    return os << p.x;
  }

  friend istream &operator>>(istream &is, ModIntR &a) {
    int64_t t;
    is >> t;
    a = ModIntR(t);
    return (is);
  }
};

// P(x_i) = y_i(i:[0,n])
//  calc c_i : P(x) = c_n x^n + c_(n-1) x^(n-1)...c_0
template <typename T>
vector<T> lagrange_interpolation(vector<T> &y,
                                 vector<T> &x) {
  assert(y.size() == x.size());
  long long n = y.size();
  vector<T> res(n, 0), Q(n), c[2];
  for(int i = 0; i < 2; ++i) c[i] = vector<T>(n, 0);
  c[0][0] = 1;
  for(int i = 0; i < n; ++i) {
    T inv = 1;
    for(int j = 0; j < n; ++j)
      if(j != i) inv *= x[i] - x[j];
    Q[i] = y[i] / inv;
    for(int j = 0; j < n; ++j) {
      c[(i + 1) % 2][j] = c[i % 2][j] * -x[i];
      if(j != 0) c[(i + 1) % 2][j] += c[i % 2][j - 1];
    }
  }
  for(int i = 0; i < n; ++i) {
    for(int j = n - 1; j >= 0; --j) {
      if(j == n - 1)
        c[(n + 1) % 2][j] = 1;
      else
        c[(n + 1) % 2][j] =
            c[n % 2][j + 1] + c[(n + 1) % 2][j + 1] * x[i];
      res[j] += c[(n + 1) % 2][j] * Q[i];
    }
  }
  return res;
}

// calc f(t) x_i = a + i * d, f(y_i) = y_i
template <typename T>
T lagrange_interpolation(const vector<T> &y, const T &t,
                         const T &a = 0, const T &d = 1) {
  long long n = y.size();
  T res = 0, p = 1;
  for(int i = 1; i < n; ++i) {
    p *= t - (a + d * i);
    p /= -d * i;
  }
  for(int i = 0; i < n; ++i) {
    if(t == a + d * i) return y[i];
    res += y[i] * p;
    p *= t - (a + d * i);
    p /= t - d * (i + 1);
    p *= d * (i - (n - 1));
    p /= d * (i + 1);
  }
  return res;
}

long long m=691;
//./a.out < data.txt でOK
int main() {
 // cin >> m;
  ModIntR ::set_mod(m);
  vector<ModIntR> a(m), b(m), res;
  int temp;
  for(int i = 0; i < m; ++i) cin >> temp >> a[i];
  for(int i = 0; i < m; ++i) b[i] = i;
  res = lagrange_interpolation<ModIntR>(a, b);
  for(int i = m-1; i >= 0; --i) {
    //if(i != 0) cout << " ";
    //cout << res[i];
    printf("%s",&res[i]);
  }
  cout << endl;
  return 0;
}
