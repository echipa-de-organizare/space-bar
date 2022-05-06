import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowEvent;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class Screen extends JPanel implements ActionListener {
    Timer creditTimer = new Timer(0, this);
    String text;
    int textY = Toolkit.getDefaultToolkit().getScreenSize().height - 50;
    JFrame window;

    public Screen() {
        GraphicsEnvironment graphics = GraphicsEnvironment.getLocalGraphicsEnvironment();
        GraphicsDevice device = graphics.getDefaultScreenDevice();
        window = new JFrame("Credits");
        window.setExtendedState(JFrame.MAXIMIZED_BOTH);
        window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        window.setLocationRelativeTo(null);
        window.add(this);
        window.setVisible(true);

        this.setBackground(Color.BLACK);
        text = """
                Credits:

                Music:
                Lala1
                Lala2
                Lala3
                Lala4


                Lala5""";
        repaint();
        creditTimer.start();
        device.setFullScreenWindow(window);
    }

    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        g2d.setFont(new Font("Arial", Font.PLAIN, 50));
        g2d.setColor(Color.WHITE);
        g2d.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        int y = textY;
        for (String line : text.split("\n")) {
            int stringLen = (int) g2d.getFontMetrics().getStringBounds(line, g2d).getWidth();
            int x = getWidth() / 2 - stringLen / 2;
            g2d.drawString(line, x, y += 60);
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
//        System.out.println(textY);
//        textY -= 5;
        textY -= 8;
        if (textY < -650) {
            creditTimer.stop();
            BufferedWriter writer;
            try {
                writer = new BufferedWriter(new FileWriter("../current_planet.txt"));//path relative to core exe!!!
                writer.write("1");
                writer.close();
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }

            window.dispatchEvent(new WindowEvent(window, WindowEvent.WINDOW_CLOSING));
        }
        repaint();
    }
}
