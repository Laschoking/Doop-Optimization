import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class BasicMethod
{
	public static void main(String[] args) throws IOException{
		(new BasicMethod()).test(args.length);
                BufferedReader buffer = new BufferedReader(
                       new InputStreamReader(System.in)
                );
                String line=buffer.readLine();
                sanitize(line);
                String result = args[0] + line;
                System.out.println(result);
	}

        static void sanitize(Object o) {

        }
    	void test(int l) {
    	}
}