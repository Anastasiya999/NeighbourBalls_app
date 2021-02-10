package mandelbrot;

import complex.Complex;
import javafx.event.ActionEvent;
import javafx.geometry.Rectangle2D;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.effect.BlendMode;
import javafx.scene.image.*;
import javafx.scene.input.MouseEvent;
import javafx.scene.paint.Color;

public class Controller{
    public Label label;											// Etykieta
    public Canvas canvas;										// "PĹĂłtno" do rysowania
    private GraphicsContext gc;// Kontekst graficzny do "pĹĂłtna"
    public TextField r;
    public Label X;
    public Label Y;
    public Label zakres;
    public TextField Width;
    public TextField Height;
    private double x1, y1, x2, y2;
    public int R=4;
    int size =512;
    private double pix_X=size;
    private double pix_Y=size;
    private double sizeH=size;
    private double sizeW=size;
    Complex a;
    Complex b ;

    public void initialize() {
        gc = canvas.getGraphicsContext2D();
        clear(gc);
    }
    private void clear(GraphicsContext gc) {
        gc.setFill(Color.WHITE);
        gc.setGlobalBlendMode(BlendMode.SRC_OVER);
        gc.fillRect(0, 0, canvas.getWidth(), canvas.getHeight());
    }
    private void rect(GraphicsContext gc) {						// Metoda rysuje prostokÄt o rogach (x1, y1) i (x2, y2)
        double x = x1;
        double y = y1;
        double w = x2 - x1;
        double h = y2 - y1;

        if (w < 0) {
            x = x2;
            w = -w;
        }

        if (h < 0) {
            y = y2;
            h = -h;
        }

        gc.strokeRect(x + 0.5, y + 0.5, w, h);
    }

    public void mouseMoves(MouseEvent mouseEvent) {
        double x = mouseEvent.getX();
        double y = mouseEvent.getY();
        gc.setGlobalBlendMode(BlendMode.DIFFERENCE);
        gc.setStroke(Color.WHITE);
        rect(gc);
        x2 = x;
        y2 = y;
        rect(gc);
    }


    public void mousePressed(MouseEvent mouseEvent) {
        x1 = mouseEvent.getX();
        y1 = mouseEvent.getY();
        x2 = x1;
        y2 = y1;
    }

    public void mouseReleased(MouseEvent mouseEvent) {
        rect(gc);
        System.out.format("%f %f %f %f\n", x1, y1, x2, y2);
        increase(gc);

    }

    public void clearCanvas(ActionEvent actionEvent) {
        clear(gc);
    }

    public void drawRect(ActionEvent actionEvent) {
        gc.setStroke(Color.web("#FFF0F0"));
        gc.setGlobalBlendMode(BlendMode.MULTIPLY);
        gc.strokeRect(100.5, 100.5, 200, 200);

    }

    public void draw(ActionEvent actionEvent) {
        final int size = 512;
        WritableImage wr = new WritableImage(size, size);
        PixelWriter pw = wr.getPixelWriter();

        for (int x = 0; x < size; x++) {
            for (int y = 0; y < size; y++) {
                pw.setArgb(x, y, (x & y) == 0 ? 0xFFFF00FF : 0xFFFFFFFF);	// Rysuje trĂłjkÄt SierpiĹskiego
            }
        }

        gc.setGlobalBlendMode(BlendMode.SRC_OVER);
        gc.drawImage(wr, 0, 0, 512, 512);
    }

    public void sayHello(ActionEvent actionEvent) {
        label.setText("Hello");
    }

    public void drawFractal(ActionEvent actionEvent) {

        if(!(r.getText().equals(""))) {
            R=Integer.parseInt(r.getText());
        }
        else
            R=4;
        if(!(Width.getText().equals(""))&&!(Height.getText().equals("")))
        {
            sizeW=Double.parseDouble(Width.getText());
            sizeH=Double.parseDouble(Height.getText());
        }
        MandelFractal mandelFractal=new MandelFractal(R);
        WritableImage wr = new WritableImage((int)sizeW, (int)sizeH);
        PixelWriter pw = wr.getPixelWriter();
        a =new Complex(-2.5, 2.5);
        b =new Complex(2.5, -2.5);

        mandelFractal.draw(pw,a,b,(int)sizeW,(int)sizeH);
        gc.setGlobalBlendMode(BlendMode.SRC_OVER);
        gc.drawImage(wr, 0, 0, 512, 512);
    }
    private void increase(GraphicsContext gc) {
        if(!(r.getText().equals(""))) {
            R=Integer.parseInt(r.getText());
        }
        MandelFractal mandelFractal=new MandelFractal(R);
        WritableImage wr = new WritableImage(size, size);
        PixelWriter pw = wr.getPixelWriter();
        double width=Math.max((x2-x1),(y2-y1));
        double X2=x1+width;
        double Y2=y1+width;
        double ax=((b.re()-a.re())/pix_X)*x1+a.re();
        double ay=((b.im()-a.im())/pix_Y)*y1+a.im();
        double bx=((b.re()-a.re())/pix_X)*X2+a.re();
        double by=((b.im()-a.im())/pix_Y)*Y2+a.im();
        a =new Complex(ax, ay);
        b =new Complex(bx, by);

        mandelFractal.draw(pw,a,b,size,size);
        gc.setGlobalBlendMode(BlendMode.SRC_OVER);
        gc.drawImage(wr,0,0,size,size);
    }


    }
