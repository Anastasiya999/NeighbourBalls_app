package complex;
import java.math.RoundingMode;

import java.text.DecimalFormat;
public class Complex implements Field<Complex> {
    private static DecimalFormat df = new DecimalFormat("0.0");
    private double r, i;

    /**
     * konstruktor inicjalizujacy
     */
    public Complex() {
        this.r = 0.0;
        this.i = 0.0;
    }

    /**
     *Konstruktor dla class Complex,ktory inicjaluzuje czesc rzeczywista
     * @param x  typu double
     */
    public Complex(double x) {
        this.r = x;
        this.i = 0;
    }

    /**
     * Konstruktor inicjalizyjacy dla class Complex
     * @param x typu double
     * @param y typu double
     */
    public Complex(double x, double y) {
        this.r = x;
        this.i = y;
    }

    /**
     * Konstruktor ktory inicjalizuje nowa liczbe Complex wartosciami innej liczby, ktora jest parametrem(kopiujacy)
     * @param x typu Complex
     */
    public Complex(Complex x) {
        this.r = x.r;
        this.i = x.i;
    }

    /**
     * Przeladowany konstruktor klasy Complex, ktory zwraca objekt klasy Complex, zainicjalizowany wartosciami z napisu
     * @param s typu String
     */
    public Complex(String s) {
        this.r = Complex.valueOf(s).re();
        this.i = Complex.valueOf(s).im();
    }

    /**
     * metoda publiczna ktora dodaje dwie liczby typu Complex
     * @param x typu Complex
     * @return obiekt typu Complex
     */
    @Override
    public Complex add(Complex x)    // Dodawanie
    {
        Complex a = this;
        double re = a.r + x.r;
        double im = a.i + x.i;
        return new Complex(re, im);
    }

    /**
     * metoda publiczna ktora odejmuje dwie liczby typu Complex
     * @param x typu Complex
     * @return objekt typu Complex
     */
    @Override
    public Complex sub(Complex x) // Odejmowanie
    {
        Complex a = this;
        double re = a.r - x.r;
        double im = a.i - x.i;
        return new Complex(re, im);
    }

    /**
     * metoda publiczna ktora mnoy dwie liczby typu Complex
     * @param x typu Complex
     * @return objekt typu Complex
     */
    @Override
    public Complex mul(Complex x)   // Mnożenie
    {
        Complex a = this;
        double re = a.r * x.r - a.i * x.i;
        double im = a.r * x.i + a.i * x.r;
        return new Complex(re, im);
    }

    /**
     * metoda publiczna ktora dzieli dwie liczby typu Complex
     * @param x typu Complex
     * @return object typu Complex
     * @throws DivideByZeroException przy dzieleniu przez zero wyruca wyjatek typu DivideByZeroException
     */
    @Override
    public Complex div(Complex x) throws DivideByZeroException// Dzielenie
    {
        Complex a = this;
        double dlugosc = x.r * x.r - x.r * x.i + x.i * x.r + x.i * x.i;
        if (dlugosc == 0) throw new DivideByZeroException(this.toString(), x.toString());
        double re = a.r * x.r + a.i * x.i;
        double im = (a.i * x.r - a.r * x.i);
        return new Complex(re / dlugosc, im / dlugosc);
    }

    /**
     * metoda publiczna ktora oblicz modul liczby typu Complex
     * @return liczbe typu double
     */
    public double abs()  // Moduł
    {
        return Math.hypot(this.r, this.i);
    }

    /**
     * metoda publiczna ktora oblicza kwadrat modulu liczby typu Complex
     * @return lliczbe typu double
     */
    public double sqrAbs()    // Kwadrat modułu
    {
        return this.abs() * this.abs();
    }

    /**
     * metoda publiczna ktora zwraca kat liczby typu Complex
     * @return liczbe typu double
     */
    public double phase()  // Faza         //sprawdzic dzielenie
    {
        return Math.atan2(this.i, this.r);

    }

    /**
     * metoda publiczna ktora zwraca czesc rzeczywista liczby typ Complex
     * @return liczbe typu double
     */
    public double re()  // Część rzeczywista
    {
        return this.r;
    }

    /**
     * metoda publiczna ktora zwraca czesz urojona liczby typu Complex
     * @return liczbe typu double
     */
    public double im()  // Część urojona
    {
        return this.i;
    }

    /**
     * metoda publiczna ktora konwertuje liczbe typu Complex w objekt typu String
     * @return Zwraca String z zapisana liczba zespolona formacie "-1.23+4.56i"
     */
    public String toString() {
        if (this.i == 0) return df.format(this.r) + "";
        if (this.r == 0) return df.format(this.i) + "i";
        if (this.i < 0) return df.format(this.r) + "-" + df.format(-this.i) + "i";
        return df.format(this.r) + "+" + df.format(this.i) + "i";
    }
    /* Zwraca String z zapisaną
        liczbą zespoloną formacie "-1.23+4.56i" */

    /**
     * metoda statyczna ktora zwraca objekt typu Complex z napisu typu String
     * @param s liczba zespolona zapisana w formacie napisu typu String
     * @return liczbe typu Complex
     */
    static Complex valueOf(String s) {
        double r;
        double i;

      if(s.contains("i"))
      {
          if(s.contains("+")) {
              String x[] = s.split("[+i]");
              if (x.length == 2) {
                  r = (Double.parseDouble(x[0]));
                  i = (Double.parseDouble(x[1]));
                  return new Complex(r, i);
              } else if (x.length == 1) {
                  i = (Double.parseDouble(x[0]));
                  return new Complex(0, i);
              } else {
                  return new Complex();
              }
          }
          else{

              String x[] = s.split("[-+i]");
              if(x.length==3) {
                  r = -(Double.parseDouble(x[1]));
                  i = -(Double.parseDouble(x[2]));
                  return new Complex(r, i);
              }else if(x.length==2){
                  r = (Double.parseDouble(x[0]));
                  i = -(Double.parseDouble(x[1]));
                  return new Complex(r, i);
              }
              else{
                  i = (Double.parseDouble(x[0]));
                  return new Complex(0, i);
              }
          }
      }
      else
      {
          String x[]=s.split("[i+]");
          r=(Double.parseDouble(x[0]));
          return new Complex(r, 0);
      }
    }
    public void setRe(double x) {
        this.r = x;
    }
    /* Przypisuje podaną wartość części rzeczywistej */

    public void setIm(double x) {
        this.i = x;
    }
    /* Przypisuje podaną wartość części urojonej */

    /**
     * przypisuje podano wartosc czesci urojonej
     * @param x typu Complex
     */
    void setVal(Complex x) {
        this.r = x.r;
        this.i = x.i;
    }

    /**
     * przypisuje podano nowe wartosci objektu typu Complex
     * @param a typu double, czesc rzeczywista
     * @param b typu double, czesc urojona
     */
    void setVal(double a, double b) {
        this.r = a;
        this.i = b;
    }

    /**
     * metoda statyczna ktora dodaje dwa objekty typu Complex
     * @param a typu Complex
     * @param b typu Complex
     * @return  objekt typu Complex
     */
    public static Complex add(Complex a, Complex b) {

        double re = a.r + b.r;
        double im = a.i + b.i;
        return new Complex(re, im);
    }

    /**
     * metoda statyczna ktora odejmuje dwie liczby typu Complex
     * @param a typu Complex
     * @param b typu Complex
     * @return objekt typu Complex
     */
    static Complex sub(Complex a, Complex b) {

        double re = a.r - b.r;
        double im = a.i - b.i;
        return new Complex(re, im);
    }

    /**
     * metoda statyczna ktora mnozy dwie liczby typu Complex
     * @param a typu Complex
     * @param b typu Complex
     * @return liczbe typu Complex
     */
    static Complex mul(Complex a, Complex b) {

        double re = a.r * b.r - a.i * b.i;
        double im = a.r * b.i + a.i * b.r;
        return new Complex(re, im);
    }

    /**
     * metoda statyczna ktora dzieli dwie liczby typu Complex i zwraca wyjatek przy dzieleniu na 0
     * @param a argument typu Complex
     * @param b argument typu Complex
     * @return zwraca liczby typu Complex ktora jest wynikiem dzielenia pierwszego argumenta przez drugi
     * @throws DivideByZeroException
     */
    static Complex div(Complex a, Complex b) throws DivideByZeroException {

        double dlugosc = b.r * b.r - b.r * b.i + b.i * b.r + b.i * b.i;
        if (dlugosc == 0) throw new DivideByZeroException(a.toString(), b.toString());
        double re = a.r * b.r + a.i * b.i;
        double im = (a.i * b.r - a.r * b.i);
        return new Complex(re / dlugosc, im / dlugosc);
    }

    static double abs(Complex a) {
        return Math.hypot(a.r, a.i);
    }

    static double phase(Complex a) {
        return Math.atan2(a.i, a.r);
    }

    static double sqrAbs(Complex a) {
        return a.abs() * a.abs();
    }

    static double re(Complex a) {
        return a.r;
    }

    static double im(Complex a) {
        return a.i;
    }

    /* Przypisuje podaną wartość */
    public static void main(String[] args) {
        Complex a = new Complex(1.0, -1.0);
        Complex b = new Complex(1.0, 1.0);
        System.out.println("a            = " + a);
        System.out.println("b            = " + b);
        System.out.println("Re(a)        = " + a.re());
        System.out.println("Im(a)        = " + a.im());
        System.out.println("b + a        = " + b.add(a).toString());
        System.out.println("a - b        = " + a.sub(b).toString());
        System.out.println("a * b        = " + a.mul(b));
        try {
            System.out.println("a / b        = " + a.div(b).toString());
        } catch (DivideByZeroException e) {
            System.out.println(e.getMessage());
        }
        System.out.println("|a|          = " + a.abs());
        System.out.println("argument       = " + a.phase());
        System.out.println(Complex.valueOf("3.7-4.7i"));

    }
}