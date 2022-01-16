package views;

import java.awt.*;

import javax.swing.*;

import models.*;

public class Window extends JFrame {
    private JPanel actualPanel;
    
    public Window() {
        this.setTitle("Picture Bot");
        this.setPreferredSize(new Dimension(500,650));
        this.setMaximumSize(new Dimension(500,650));
        this.setResizable(false);
		// this.setLocationRelativeTo(null);
        this.setDefaultCloseOperation(EXIT_ON_CLOSE);
        actualPanel = new HomePanel(this);
        actualPanel.setBorder(BorderFactory.createMatteBorder(6, 6, 6, 6, Color.blue));
        this.setContentPane(actualPanel);
    }
    
    public JPanel getActualPanel() {
        return actualPanel;
    }

    public void updateView() {
        revalidate();
        repaint();
    }

    public void setHomePanel() {
        this.getContentPane().removeAll();
        this.actualPanel = new HomePanel(this);
        actualPanel.setBorder(BorderFactory.createMatteBorder(6, 6, 6, 6, Color.blue));
        this.setContentPane(actualPanel);
        this.updateView();
    }

    public void setSettingsPanel() {
        this.getContentPane().removeAll();
        this.actualPanel = new SettingsPanel(this, new SettingsModel());
        actualPanel.setBorder(BorderFactory.createMatteBorder(6, 6, 6, 6, Color.blue));
        this.setContentPane(actualPanel);
        this.updateView();
    }

    public void setEditPanel(String member, String era) {
        this.getContentPane().removeAll();
        EditModel model = new EditModel(member, era);
        this.actualPanel = new EditPanel(this, model);
        actualPanel.setBorder(BorderFactory.createMatteBorder(6, 6, 6, 6, Color.blue));
        this.setContentPane(actualPanel);
        this.updateView();
    }
}