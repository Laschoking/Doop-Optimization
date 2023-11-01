import java.io.*;

public class Example_1
{
    public static void main(final String[] args) throws IOException {
        int i;
        int sum = 0;
        int count = 5;
        for (i = 0; i < count; i++){

	sum = add(sum, i);
    }
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
    
  
