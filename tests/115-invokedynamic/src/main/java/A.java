import java.lang.invoke.*;

// This class must be in a separate file or the invokedynamic
// bootstrap procedure fails.
public class A {
    public static Integer staticMeth() {
        System.out.println("staticMeth() called.");
        return new Integer(10);
    }

    public void methI(Integer i) {
        System.out.println("this.methI(" + i + ") called, this = " + this.hashCode());
    }

    public Double doubleIdentity(Double d) {
        System.out.println("doubleIdentity(" + d + ") called.");
        return d;
    }

    public Double add3(Integer a, Float b, Short c) {
        Double sum = a.doubleValue() + b.doubleValue() + c.doubleValue();
        System.out.println("add3: " + a + " + " + " + " + b + " + " + c + " = " + sum);
        return sum;
    }

    public static CallSite bootstrap(MethodHandles.Lookup caller, String name, MethodType type)
                           throws NoSuchMethodException, IllegalAccessException {
        MethodType mt = MethodType.methodType(Void.TYPE, A.class);
        MethodHandle handle = MethodHandles.lookup().findStatic(A.class, name, mt);
        return new ConstantCallSite(handle);
    }
    public static CallSite bootstrap2(MethodHandles.Lookup caller, String name, MethodType type)
                           throws NoSuchMethodException, IllegalAccessException {
        MethodHandle handle = MethodHandles.lookup().findStatic(A.class, name, type);
        return new ConstantCallSite(handle);
    }
    public static CallSite bootstrap3(MethodHandles.Lookup caller, String name, MethodType type)
                           throws NoSuchMethodException, IllegalAccessException {
        Class<?> c;
        try {
            c = Class.forName("Unknown");
        } catch (ClassNotFoundException ex) {
            c = A.class;
        }
        MethodHandle handle = MethodHandles.lookup().findStatic(c, name, type);
        return new ConstantCallSite(handle);
    }
    public static CallSite bootstrap4(MethodHandles.Lookup caller, String name, MethodType type)
                           throws NoSuchMethodException, IllegalAccessException {
        MethodType mt = MethodType.methodType(Void.TYPE, A.class);
        MethodHandle handle = MethodHandles.lookup().findVirtual(A.class, name, mt);
        return new ConstantCallSite(handle);
    }

    public static void print(A a) {
        Integer i = a.staticMeth();
    }

    public void print2(A a) {
        Integer i = a.staticMeth();
        int hash = this.hashCode();
        System.out.println("print2() called, i = " + i + ", hash code = " + hash);
    }

    public void add3_dynamic() throws Throwable {
        System.out.println("== add3_dynamic ==");

        MethodType mType = MethodType.methodType(Double.class, Integer.class, Float.class, Short.class);
        MethodHandles.Lookup lookup = MethodHandles.lookup();
        MethodHandle add3_mh = lookup.findSpecial(A.class, "add3", mType, A.class);
        Main.info(add3_mh, mType);
        Double d = (Double)add3_mh.invokeExact(this, new Integer(11), new Float(112.0), new Short("1"));
        System.out.println("add3_dynamic() | Result: d = " + d);
    }

    public A init_dynamic() throws Throwable {
        System.out.println("== init_dynamic ==");
        MethodType mType = MethodType.methodType(void.class);
        MethodHandles.Lookup lookup = MethodHandles.lookup();
        MethodHandle constr = lookup.findConstructor(Class.forName("A"), mType);
        A a = (A)constr.invokeExact();
        System.out.println("A: " + a.hashCode());
        return a;
    }

    public void test() throws Throwable {
        add3_dynamic();
        A a = init_dynamic();
    }

    public A() {
        System.out.println("A() called.");
    }
}
