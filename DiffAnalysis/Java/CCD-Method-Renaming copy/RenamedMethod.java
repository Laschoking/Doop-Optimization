import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class RenamedMethod
{
	public static void main(String[] args) throws IOException{
		(new RenamedMethod()).test(args.length);
                BufferedReader reader = new BufferedReader(
                       new InputStreamReader(System.in)
                );
                String string=reader.readLine();
                sanitize(line);
                String output = args[0] + string;

                System.out.println(output);
	}

        static void sanitize(Object o) {
            
        }


}

