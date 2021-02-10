package complex;


public class DivideByZeroException extends Exception {
    String komunikat;
    // public DivideByZeroException(){ komunikat="";}
    public DivideByZeroException(String a, String b){
        komunikat="nie wolno dzielic "+a+"/"+b;
    }
    @Override
    public String getMessage() {
        return komunikat;
    }
}
