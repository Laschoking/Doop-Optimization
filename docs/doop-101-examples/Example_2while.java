import java.io.*;

public class Example_2while
{
    public static void main(final String[] args) throws IOException {
        new Example_2while().test(args.length);
        final BufferedReader buffer = new BufferedReader(new InputStreamReader(System.in));
        final String line = buffer.readLine();
        sanitize(line);
        final String result = args[0] + line;
        int a = 5;
        int b = 10;
        int c = 50;
        int g = b - c;
        int h,e,f,z;
        h = 0;
        z = 0;

	int i = 5;
	int k = 5;
	while (i < 10){
 		i = i + 1;
 		z = i +k;
		if (i == 8)
			h = i + k;
	}
	
	f = h;
	e = k;

    }
    
    static void sanitize(final Object o) {
    }
    
    static int moreTest(final int z, final boolean g) {
        if (g) {
            return z - 5;
        }
        return z - 3;
    }
    
    void test(final int l) {
        Animal a;
        if (l == 0) {
            a = new Cat();
        }
        else {
            a = new Dog();
        }
        a.play();
        final Cat c1 = new Cat();
        final Cat c2 = new Cat();
        c1.setParent(c2);
        this.morePlay(c1);
    }
    
    void morePlay(final Cat c) {
        final Cat p = c.getParent();
        p.play();
        final Animal a1 = p.playWith(c);
        final Animal a2 = c.playWith(p);
        if (a1 == a2) {
            return;
        }
    }
}

class Cat extends Animal
{
    Cat parent;
    
    void setParent(final Cat c) {
        this.parent = c;
    }
    
    Cat getParent() {
        return this.parent;
    }
    
    @Override
    void play() {
    }
}

class Animal
{
    void play() {
    }
    
    Animal playWith(final Animal other) {
        other.play();
        return other;
    }
}

class Dog extends Animal
{
    @Override
    void play() {
    }
}

