import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Renamed
{
	public static void main(String[] args) throws IOException{
		(new Renamed()).test(args.length);
                BufferedReader reader = new BufferedReader(
                       new InputStreamReader(System.in)
                );
                String string=reader.readLine();
                clean(line);
                String output = args[0] + string;

                System.out.println(output);
	}

        static void clean(Object o) {
            
        }


}

