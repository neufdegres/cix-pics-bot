import database.Functions;

// import javax.swing.*;

// import java.awt.*;
// import java.awt.event.*;

public class Test {
    public static void main(String[] args) {
        /* String[] groups = {"aespa", "bvndit", "cix", "pixy"};

        JFrame frame = new JFrame();
        frame.setMinimumSize(new Dimension(230, 150));
        frame.setLayout(new FlowLayout());

        JComboBox<String> jComboBox = new JComboBox<>(groups);
        JButton valider = new JButton("valider");
        JLabel label = new JLabel();

        valider.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String selectedFruit = "stan " + jComboBox.getItemAt(jComboBox.getSelectedIndex()) + " !!";
                label.setText(selectedFruit);
            }
        });


        frame.add(jComboBox);
        frame.add(valider);
        frame.add(label);

        frame.setVisible(true); */

        // int a = 15;
        // int b = 35;
        // int c = 20;

        // System.out.println(c * a / b);

        // String hh = "/home/ubuntu/picture_bot/pics/5/213.jpg".substring(30);
        // System.out.println(hh);

        var map = Functions.getErasFromDB();
        System.out.println(map.toString());

    }
}
