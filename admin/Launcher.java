import java.io.IOException;

import javax.swing.SwingUtilities;

import views.Window;

public class Launcher {
    public static void main(String[] args) throws IOException {
        SwingUtilities.invokeLater(() -> {
            Window jeu;
            jeu = new Window();
            jeu.pack();
            jeu.setVisible(true);
        });
    }
}