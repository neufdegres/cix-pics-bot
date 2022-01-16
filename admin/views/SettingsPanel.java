package views;

import java.awt.*;

import javax.swing.*;
import javax.swing.border.EmptyBorder;

import controllers.SettingsController;
import models.SettingsModel;

public class SettingsPanel extends JPanel {
    private Window frame;
    private SettingsModel model;
    private SettingsController controller;
    private JLabel title;
    private JPanel top, content, member, era, confirmPanel, backPanel;
    private JLabel memberLabel, eraLabel;
    private JComboBox<String> memberBox, eraBox;
    private JButton confirm, back;

    public SettingsPanel(Window f, SettingsModel m) {
        this.frame = f;
        this.model = m;
        this.controller = new SettingsController(this);
        this.setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
        title = new JLabel("Setting Research");
        title.setFont(new Font("Arial", 1, 40));
        top = new JPanel();
        top.setMaximumSize(new Dimension(500, 100));
        top.setPreferredSize(new Dimension(500, 100));
        top.setBorder(new EmptyBorder(20, 0, 0, 0));
        top.add(title);
        memberLabel = new JLabel("member");
        memberLabel.setFont(new Font("Arial", 0, 25));
        memberBox = new JComboBox<>(model.getMembers());
        member = new JPanel();
        member.setLayout(new GridLayout(2,1));
        member.setMaximumSize(new Dimension(300, 100));
        member.setPreferredSize(new Dimension(300, 100));
        member.add(memberLabel);
        member.add(memberBox);
        eraLabel = new JLabel("era");
        eraLabel.setFont(new Font("Arial", 0, 25));
        eraBox = new JComboBox<>(model.getEras());
        era = new JPanel();
        era.setLayout(new GridLayout(2,1));
        era.setMaximumSize(new Dimension(300, 100));
        era.setPreferredSize(new Dimension(300, 100));
        era.add(eraLabel);
        era.add(eraBox);
        confirm = new JButton("confirm");
        confirm.setPreferredSize(new Dimension(250, 60));
        confirm.setMaximumSize(new Dimension(250, 60));
        confirmPanel = new JPanel();
        confirmPanel.setBorder(new EmptyBorder(50, 0, 0, 0));
        confirmPanel.setMaximumSize(new Dimension(500, 170));
        confirmPanel.setPreferredSize(new Dimension(500, 170));
        back = new JButton("back");
        back.setPreferredSize(new Dimension(170, 50));
        back.setMaximumSize(new Dimension(170, 50));
        iniButtons();
        backPanel = new JPanel();
        confirmPanel.add(confirm);
        backPanel.add(back);
        content = new JPanel();
        content.setLayout(new BoxLayout(content, BoxLayout.Y_AXIS));
        content.setMaximumSize(new Dimension(500, 550));
        content.setPreferredSize(new Dimension(500, 550));
        content.add(member);
        content.add(era);
        content.add(confirmPanel);
        content.add(backPanel);
        this.add(top);
        this.add(content);
    }

    private void iniButtons() {
        confirm.addActionListener((event) -> {
            JButton b = (JButton) event.getSource();
            if(b.isEnabled()) controller.confirmPressed();
        });
        back.addActionListener((event) -> {
            JButton b = (JButton) event.getSource();
            if(b.isEnabled()) controller.backPressed();
        });
    }

    public Window getFrame() {
        return frame;
    }

    public JComboBox<String> getMemberBox() {
        return memberBox;
    }

    public JComboBox<String> getEraBox() {
        return eraBox;
    }

}
