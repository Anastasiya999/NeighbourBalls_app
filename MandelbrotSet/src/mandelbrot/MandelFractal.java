package mandelbrot;
import complex.Complex;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.effect.BlendMode;
import javafx.scene.image.PixelWriter;
import javafx.scene.image.WritableImage;
import javafx.scene.paint.Color;

import static javafx.scene.paint.Color.*;

public class MandelFractal implements ComplexDrawable {
    /*private GraphicsContext gc;
    public  MandelFractal(GraphicsContext gc){
         this.gc=gc;
     }*/
    private int R;
    public  MandelFractal(int R){
        this.R=R;
    }

     public void draw(PixelWriter pw, Complex a, Complex b, int w, int h) {
        double reMin = a.re();
        double reMax = b.re();
        double imMin = a.im();
        double imMax = b.im();
        int maxIterations = 300;
        Complex c = new Complex();
        Complex z = new Complex();
        double width=Math.max(w,h);
        double pixelX = (reMax - reMin) / (width-1);
        double pixelY = (imMax - imMin) / (width-1);
        for(int y=0;y<width;y++)
        {
            for(int x=0; x<width;x++)
            {
                c.setRe(x*pixelX+reMin);
                c.setIm(y*pixelY+imMin);
                z.setIm(0.0);
                z.setRe(0.0);
                int count=0;
                while((z.sqrAbs()<R)&&(count<maxIterations))
                {
                    z=z.mul(z).add(c);
                    count++;
                }
                if (count < maxIterations) {
                    //Color [] colors ={AQUAMARINE,	DARKORCHID,	DARKSLATEBLUE,	INDIGO,	DARKRED,	CHOCOLATE,	GOLD,LAWNGREEN,SLATEBLUE,	YELLOWGREEN,	KHAKI};
                    Color [] colors ={	DARKORCHID,		DARKRED,	CHOCOLATE,	GOLD,LAWNGREEN,	YELLOWGREEN,	KHAKI};
                    pw.setColor(x,y,colors[count%7]);

                }
                else
                    pw.setColor(x,y,Color.BLACK);
            }
        }

    }

}




