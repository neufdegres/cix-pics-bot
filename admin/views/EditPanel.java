package views;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;
import javax.swing.*;
import javax.swing.border.EmptyBorder;

import controllers.EditController;
import database.Pic;
import models.EditModel;

public class EditPanel extends JPanel {
    private Window frame;
    private EditModel model;
    private EditController controller;
    private ImagePanel img;
    private JPanel titlePanel, content, memberPanel, eraPanel, choix, bottom;
    private JLabel title, titleValue, member, memberValue, era, eraValue;
    private JComboBox<String> eraBox;
    private JButton edit, back, next, goSettings;
    private Action leftAction, rightAction, enterAction;

    public EditPanel(Window f, EditModel m) {
        this.frame = f;
        this.model = m;
        this.controller = new EditController(this, model);
        this.setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
        this.setFocusable(true);
        this.requestFocusInWindow();
        title = new JLabel("photo #");
        title.setFont(new Font("Arial", 1, 30));
        titleValue = new JLabel("0000");
        titleValue.setFont(new Font("Arial", 1, 35));
        titlePanel = new JPanel();
        titlePanel.setBorder(new EmptyBorder(10, 0, 0, 0));
        titlePanel.add(title);
        titlePanel.add(titleValue);
        img = new ImagePanel();
        member = new JLabel("member");
        member.setFont(new Font("Arial", 1, 20));
        member.setBorder(new EmptyBorder(0, 0, 0, 15));
        memberValue = new JLabel("-");
        memberValue.setFont(new Font("Arial", 0, 20));
        memberPanel = new JPanel();
        memberPanel.setPreferredSize(new Dimension(300, 25));
        memberPanel.add(member);
        memberPanel.add(memberValue);
        era = new JLabel("era");
        era.setFont(new Font("Arial", 1, 20));
        era.setBorder(new EmptyBorder(0, 0, 0, 15));
        String[] eraLabels = model.getEras();
        eraBox = new JComboBox<>(eraLabels);
        eraBox.setSelectedItem("wave");
        eraValue = new JLabel(" ( - )");
        eraValue.setFont(new Font("Arial", 2, 15));
        eraPanel = new JPanel();
        eraPanel.setPreferredSize(new Dimension(300, 25));
        eraPanel.add(era);
        eraPanel.add(eraBox);
        eraPanel.add(eraValue);
        content = new JPanel();
        content.setLayout(new BoxLayout(content, BoxLayout.Y_AXIS));
        content.setBorder(new EmptyBorder(15, 0, 0, 0));
        content.add(memberPanel);
        content.add(eraPanel);
        back = new JButton("<");
        edit = new JButton("edit");
        next = new JButton(">");
        goSettings = new JButton("back");
        iniButtons();
        iniActions();
        choix = new JPanel();
        choix.add(back);
        choix.add(edit);
        choix.add(next);
        bottom = new JPanel();
        bottom.add(goSettings);
        this.add(titlePanel);
        this.add(img);
        this.add(content);
        this.add(choix);
        this.add(bottom);
        updatePanel();
    }

    private void iniButtons() {
        back.setEnabled(false);
        back.addActionListener((event) -> {
            JButton b = (JButton) event.getSource();
            if(b.isEnabled()) controller.backPressed();
        });
        next.setEnabled(false);
        next.addActionListener((event) -> {
            JButton b = (JButton) event.getSource();
            if(b.isEnabled()) controller.nextPressed();
        });
        edit.setEnabled(false);
        edit.addActionListener((event) -> {
            JButton b = (JButton) event.getSource();
            if(b.isEnabled()) controller.editPressed();
        });
        goSettings.addActionListener((event) -> {
            JButton b = (JButton) event.getSource();
            if(b.isEnabled()) controller.goSettingsPressed();
        });
    }

    public void iniActions() {
        leftAction = new LeftAction();
        rightAction = new RightAction();
        enterAction = new EnterAction();
        this.getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke("LEFT"), "setBack");
        this.getActionMap().put("setBack", leftAction);
        this.getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke("RIGHT"), "setNext");
        this.getActionMap().put("setNext", rightAction);
        this.getInputMap(WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke("ENTER"), "edit");
        this.getActionMap().put("edit", enterAction);
    }

    public Window getFrame() {
        return frame;
    }

    public JComboBox<String> getEraBox() {
        return eraBox;
    }

    public JButton getEdit() {
        return edit;
    }

    public JButton getBack() {
        return back;
    }

    public JButton getNext() {
        return next;
    }
    
    public void updatePanel() {
        Pic image = model.getActual();
        if(image == null) return;
        titleValue.setText(String.valueOf(image.getId()));
        img.setImage(image.getPath());
        memberValue.setText(image.getMember());
        if(image.getEra() != null) eraValue.setText(" (" + image.getEra() + ")");
        else eraValue.setText(" ( - )");
        edit.setEnabled(true);
        if(model.isBack()) back.setEnabled(true);
        else back.setEnabled(false);
        if(model.isNext()) next.setEnabled(true);
        else next.setEnabled(false);
        frame.updateView();
    }

    class ImagePanel extends JPanel {
        private BufferedImage raw;
        private JLabel image;

        public ImagePanel() {
            this.setMaximumSize(new Dimension(380, 380));
            this.setPreferredSize(new Dimension(380, 380));
            this.setBorder(BorderFactory.createMatteBorder(2, 2, 2, 2, Color.blue));
            this.setLayout(new FlowLayout());
            image = new JLabel();
            setImage();
            this.add(image);
        }

        public void setImage(String src) {
            try {
                raw = ImageIO.read(new File(src));
                int[] newDim = resizeImage();
                Image dimg = raw.getScaledInstance(newDim[0], newDim[1],
                Image.SCALE_SMOOTH);
                image.setIcon(new ImageIcon(dimg));
            } catch (IOException e) {
                System.out.println("Impossible de trouver l'image");
                e.printStackTrace();
            }
        }

        public void setImage() {
            setImage("/home/vicky/Projets/twitterBots/Picturebot/admin/views/resources/ntd.png");
        }

        private int[] resizeImage() { // 0 : width; 1 : height; 
            int[] dim = {raw.getWidth(), raw.getHeight()};
            int max = 364;
            int bgstSide = Math.max(dim[0], dim[1]);
            dim[0] = dim[0] * max / bgstSide;
            dim[1] = dim[1] * max / bgstSide;
            return dim;
        }

        
    }

    class LeftAction extends AbstractAction {
        @Override
        public void actionPerformed(ActionEvent e) {
            if(back.isEnabled()) controller.backPressed();
        }
    }

    class RightAction extends AbstractAction {
        @Override
        public void actionPerformed(ActionEvent e) {
            if(next.isEnabled()) controller.nextPressed();
        }
    }

    class EnterAction extends AbstractAction {
        @Override
        public void actionPerformed(ActionEvent e) {
            if(edit.isEnabled()) controller.editPressed();
        }
    }

}
