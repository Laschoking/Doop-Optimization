#include <cstdint>
#include <cfloat>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <iostream>


extern "C" {

float str_to_float(const char* x) {
    double j  = 1.1;
    char g[strlen(x)];
    //const char* g = *x;
    const char c = 'L';
    if (strchr(x, c)!= NULL){
        j = 2.1;
        int i = 0;
        while(i <strlen(x)){
            if (x[i]!= 'L')
                g[i]=x[i];
            i++;

        }
        return atof(g);
    }else {
        return atof(x);

}
}

int testId(int i){
    return i;
}



}

