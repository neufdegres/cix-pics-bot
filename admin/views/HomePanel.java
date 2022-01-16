package views;

import java.awt.*;

import javax.swing.*;
import javax.swing.border.EmptyBorder;

import controllers.HomeController;

public class HomePanel extends JPanel {
    private Window frame;
    private HomeController controller;
    private JPanel top, bottom;
    private JLabel title;
    private JButton ajouter, modifier;

    public HomePanel(Window v) {
        this.frame = v;
        this.controller = new HomeController(this);
        this.setLayout(new GridLayout(2,1));
        title = new JLabel("<html><p style=\"text-align: center;\">Picture bot<br>administration</p></html>");
        title.setFont(new Font("Arial", 1, 40));
        top = new JPanel();
        top.setBorder(new EmptyBorder(110, 0, 0, 0));
        top.add(title);
        ajouter = new JButton("add a new picture");
        ajouter.setPreferredSize(new Dimension(400, 80));
        modifier = new JButton("edit existing pics");
        modifier.setPreferredSize(new Dimension(400, 80));
        iniButtons();
        bottom = new JPanel();
        bottom.setLayout(new FlowLayout(1, 0, 20));
        bottom.add(ajouter);
        bottom.add(modifier);
        this.add(top);
        this.add(bottom);
    }

    private void iniButtons() {
        modifier.addActionListener((event) -> {
            JButton b = (JButton) event.getSource();
            if(b.isEnabled()) controller.editPressed();
        });
    }

    public Window getFrame() {
        return frame;
    }
}
