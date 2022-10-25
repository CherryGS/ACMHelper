#include <bits/stdc++.h>
#include "testlib.h"
using namespace std;

/*
    inf : input
    ouf : user output
    ans : answer output

    _ok : Accept
    _wa : Wrong Answer
*/

int main(int argc,char** argv) {
    registerTestlibCmd(argc,argv); // Required
    
    double pans=ouf.readDouble();
    double jans=ans.readDouble();

    if(abs(pans-jans) <= 1e-5) { quitf(_ok,"Correct!"); }
    else { quitf(_wa,"Wrong Answer!"); }
}