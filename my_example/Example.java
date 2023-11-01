import java.io.*;

public class Example
{
    public static void main(final String[] args) throws IOException {
        new Example().test(args.length);
        final BufferedReader buffer = new BufferedReader(new InputStreamReader(System.in));
        final String line = buffer.readLine();
        sanitize(line);
        final String result = args[0] + line;
        int a = 5;
        int b = 10;
        int c;
        if (b < a) {
            c = 1;
            if (b > a) { c =2;}
            else {c = 3;}
            return ;

        }else{
		c = 4;
	}

       c = 5;
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

