#include <iostream>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <cstdio>

#define MAX_EMPLY 100
#define MAX_MEET 100
#define __OPENFILE freopen("./problem.txt", "r", stdin);

using namespace std;

vector<int> explode(const string &delimiter, const string &str) {
    int len = str.length();
    int dlen = delimiter.length();
    vector<int> arr;

    if (0 == dlen) return arr;
    int i = 0, k = 0;

    for (i = 0; i < len; ++i){
        if (str.substr(i, dlen) != delimiter) continue;
        arr.push_back(atoi(str.substr(k, i - k).c_str()));
        i += dlen;
        k = i;
    }
    arr.push_back(atoi(str.substr(k, i - k).c_str()));
    return arr;
}

void solve(int n_m, int n_e, int n_s, int travel[MAX_MEET][MAX_MEET], vector<int>* employee){
}

int main(){
    int         n_m; //Number of meetings
    int         n_e; //Number of employees
    int         n_s; //Number of time slots
    string      line; //temp line for reading lines
    int         travel[MAX_MEET][MAX_MEET]; // table for travaling from one meeting to another
    vector<int> employee[MAX_EMPLY];

    /* Initial the values from the problem */
    __OPENFILE

    cin >> n_m >> n_e >> n_s;

    getline(cin, line);

    for (int i = 0; i < n_e; i++ ) {
        getline(cin, line);
        employee[i] = explode(" ", line);
        cout<<line<<endl;
    }

    for (int i = 0; i < n_m; i++) {
        for (int j = 0; j < n_m; j++){
            cin >> travel[i][j];
        }
    }

    solve(n_m, n_e, n_s, travel, employee);

    return 0;
}
