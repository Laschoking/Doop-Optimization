import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Renamed
{
	public static void main(String[] args) throws IOException{
		(new Renamed()).test(args.length);
                BufferedReader in = new BufferedReader(
                       new InputStreamReader(System.in)
                );
                String s=in.readLine();
                sanitize(line);
                String ret = args[0] + s;

                System.out.println(ret);
	}

        static void sanitize(Object o) {

        }


}


