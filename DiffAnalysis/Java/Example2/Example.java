import java.io.*;

public class Example
{
    public static void main(final String[] args) throws IOException {
        int i;
        int sum = 0;
        int k = 5;
        int count = 5;
        for (i = 0; i < count; i++){

	sum = add(sum, i);
    }
    k = add(k,i);
   i = sum;
   return ;
   
   }
    static int add(int a, int b){
        if (a < b) {
        	return a + b;}
        else{
        	return a - b;
        	
    	}
 	}
 }
    
  
