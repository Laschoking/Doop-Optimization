import java.io.*;

public class Example
{
    public static void main(final String[] args) throws IOException {
        int i;
        int c = 5;
        int sum = 0;
        for (i = 0; i < c; i++){
        	if (i < sum) {
        	
        		sum = add(sum, i);}
        	else
        		{sum = add(sum, -i);
	}

    }
   i = sum;
   return ;
   
   }
    static int add(int a, int b){
    return a + b;
    }
 }
    
  
