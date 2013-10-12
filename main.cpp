/*
 * variables: time slots 
 * domains: meetings
 * constraints: employee must attend they need to (No time overlap for meetings and enough time for them to switch between meetings)
 */

#include <iostream>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <algorithm>
#include <cstdio>
#include <cmath>

#define MAX_EMPLY 100
#define MAX_MEET 100
#define __OPENFILE freopen("./problem.txt", "r", stdin);

using namespace std;

int         n_m; //Number of meetings
int         n_e; //Number of employees
int         n_s; //Number of time slots
int         travel[MAX_MEET][MAX_MEET]; // table for travaling from one meeting to another
int         meet[MAX_MEET]; //make it not zero if assigned a time slot for it
vector<int> employee[MAX_EMPLY];
int         remain[MAX_MEET]; // the remaining timeslot choice for the meeting

bool assignment_complete() {
    for(int i = 0; i < n_m; i++) {
        if(meet[i] == 0)
            return false;
    }
    return true;
}

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
bool is_needed_by_employee(int m_idx, int e_idx){
    vector<int>::iterator result = find((employee[e_idx]).begin(), (employee[e_idx]).end() ,m_idx);
    if(result == (employee[e_idx]).end())
        return false;
    else
        return true;
}
bool is_legal(int m_idx, int t_idx){
    if (meet[m_idx] != 0)
        return false;
    for (int i = 0; i < n_m; i++){
        if(meet[i] != 0){
            for (int j = 0; j < n_e; j++){
                if(is_needed_by_employee(i, j) && is_needed_by_employee(m_idx, j) ){
                    if(abs(t_idx - meet[i]) < travel[i][m_idx]){
                        return false;
                    }
                }
            }
        }
    }
    return true;
}
int mvr(){

    return 0;
}
void solve(){
    int subroot = mvr(); //Most constrained variable

}

int get_remain_val(int i){
    for (int i = 0; i < n_s; )
    return 0;
}

void set_remain_val(){
    for (int i = 0; i < n_s; i++){// I am still not sure n_s of n_m
        if(meet[i] != 0){
            remain[i] = -1;
        }
        else{
            remain[i] = get_remain_val(i);
        }
    }
}
void sign_var(int var, int value){
    meet[var] = value;
    set_remain_val();
}
int main(){
    string line; //temp line for reading lines

    /* Initial the values from the problem */
    __OPENFILE

    cin >> n_m >> n_e >> n_s;

    getline(cin, line);

    for (int i = 0; i < n_e; i++ ) {
        getline(cin, line);
        employee[i] = explode(" ", line);
    }

    for (int i = 0; i < n_m; i++) {
        for (int j = 0; j < n_m; j++){
            cin >> travel[i][j];
        }
        remain[i] = n_s;
    }

    memset(meet,0,sizeof(meet)); 
    solve();

    return 0;
}
