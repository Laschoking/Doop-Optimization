#include <cstdint>
#include <cfloat>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <iostream>
extern "C" {

float str_to_float(std::string x) {
    //std::string x = "1.1L";
    int p = x.find("L");
    if (p != std::string::npos){
        x.erase(p);
    }
    //x.c_str()
    return atof("1.1112");

}


float str_to_float1(const char* x) {
    float j;
    char g[strlen(x)];
    strcpy(g,x);
    //const char* g = *x;
    const char c = 'L';
    if (strchr(x, c)!= NULL){
        int i = 0;
        j = 2.1;
        /*while(int i = 0 <strlen(x)){
            if (x[i]!= 'L')
                ret[i]=x[i];
            i++;

        }*/
    }else {
        j = atof(g);
    }
    return j;

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



int main(){
    //std::cout << str_to_float1("1.3451L");
    std::cout << retType("4.4564");
}
}
/*

int main(){
    const char* x = "1.1L";
    char* ret;
    printf("test%s",x);
    if (strstr(x, "L"))
        int i = 0;
        while(int i = 0 <strlen(x)){
            if (x[i]!= 'L')
                ret[i]=x[i];
            i++;

        }
    printf("test%s",ret);
}
}
    */