import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class BasicMethod
{
	public static void main(String[] args) throws IOException{
		(new BasicMethod()).test(args.length);
                BufferedReader in = new BufferedReader(
                       new InputStreamReader(System.in)
                );
                String s=in.readLine();
                sanitize(s);
                String ret = args[0] + s;
                System.out.println(ret);
	}

        static void sanitize(Object o) {
            
        }
    	void test(int l) {
    	}

}

