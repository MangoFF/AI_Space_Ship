#include <cstring>
#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <map>
#include <unordered_map>
#include <queue>
#include <climits>
#include <unordered_set>
#include <algorithm>
#include <queue>

using namespace std;
typedef long long ll;

struct node{
  int p,l;
  bool operator<(const node &x)const {
    return l<x.l;
  }
};
bool work(int n,int m){
  priority_queue<node> pq;
  pq.push({1,m});
  while(n--){
    if(pq.empty())return false;
    auto a=pq.top();pq.pop();
    if(a.l<=1)return false;
    if(a.l==2){
      //cout<<a.p<<' '<<a.l<<endl;
      int c=a.p-1,d=a.p+a.l;
      if(c<=0||d>m)continue;
      else {++n;continue;}
    }else{
      int mid=a.p+(a.l-1)/2,left_l=mid-a.p;
      pq.push({a.p,left_l});
      //cout<<a.p<<' '<<left_l<<endl;
      pq.push({mid+1,a.l-left_l-1});
      //cout<<(mid+1)<<' '<<(a.l-left_l-1)<<endl;
    }
  }
  return true;
}
int go(int n){
  if(n==1)return 1;
  int l=1,h=100000,m;
  while(l<h){
    m=(l+h)/2;
    if(work(n,m))h=m;
    else l=m+1;
  }
  return l;
}
int main(){
  #ifdef BUG //调试使用，不需要写
  freopen("a.in","r",stdin); 
  #endif

  int t,n;
  cin>>t;
  while(t--){
    cin>>n;
    cout<<go(n)<<endl;
  }
}