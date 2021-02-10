package complex;

public interface Field<T> {
    T add(T x);         // dodawanie
    T sub(T x);          // odejmowanie
    T mul(T x);          // mnożenie
    T div(T x) throws DivideByZeroException;          // dzielenie
    String toString();
}
