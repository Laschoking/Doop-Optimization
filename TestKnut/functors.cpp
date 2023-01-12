#include <cstdint>
#include <cfloat>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <iostream>


extern "C" {

float str_to_float(const char* x) {
    char g[strlen(x)];
    //const char* g = *x;
    const char c = 'L';
    if (strchr(x, c)!= NULL){
        int i = 0;
        //bool exp = false; E wird gehandelt
        while(i <strlen(x)){
            if (x[i] != 'L' && x[i] != 'F')
            //davon ausgehend, dass nur 1 E gelesen wird
                /*if (x[i] == 'E'){
                    exp = true;
                }else if(exp){
                    g[i-1] = x[i];
                }*/
                g[i]=x[i];
            i++;

        }
        return atof(g);
    }else {
        return atof(x);

}
}

const char * retType(const char* x){
    int i = 0;
    const char * t = "i";
    while(x[i++] != '\0'){
        if (x[i]== '.' || x[i] == 'E'){
            t = "f";
            break;
        }

    }
return t;
}
int testId(int i){
    return i;
}



}

