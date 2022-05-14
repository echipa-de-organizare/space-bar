import javax.swing.*;
import javax.swing.filechooser.FileSystemView;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowEvent;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

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
                Credits
                                
                                
                --space bar--
                                
                Fiicode Gamedev 2022
                                
                Alexandru Negru
                Roxana Zachman
                Samuel Gherasim
                                
                Babeș-Bolyai University, Cluj-Napoca, and Technical University of Cluj-Napoca
                                
                "echipa de organizare"
                                
                                
                                
                All rights reserved.
                """;
        repaint();
        creditTimer.start();
        device.setFullScreenWindow(window);
    }

    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        g2d.setFont(new Font("Candara", Font.PLAIN, 50));
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
        textY -= 5;
//        textY -= 6;
        if (textY < -1200) {
            creditTimer.stop();
            BufferedWriter writerPlanet, writerState;
            try {
                File file = new File(FileSystemView.getFileSystemView().getDefaultDirectory().getPath() + "\\spacebarlogS.txt");
                Scanner scanner = new Scanner(file);
                int state = 0;
                if (scanner.hasNextLine()) {
                    state = Integer.parseInt(scanner.nextLine());
                }
                scanner.close();

                writerPlanet = new BufferedWriter(new FileWriter(FileSystemView.getFileSystemView().getDefaultDirectory().getPath() + "\\spacebarlogP.txt"));
                writerState = new BufferedWriter(new FileWriter(FileSystemView.getFileSystemView().getDefaultDirectory().getPath() + "\\spacebarlogS.txt"));
                if (state == 1 || state == 0) {
                    writerPlanet.write("1");
                    writerState.write("1");
                } else if (state == 3) {
                    writerPlanet.write("-1");
                }
                writerState.close();
                writerPlanet.close();
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }

            window.dispatchEvent(new WindowEvent(window, WindowEvent.WINDOW_CLOSING));
        }
        repaint();
    }
}
