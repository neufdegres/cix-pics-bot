package controllers;

import views.HomePanel;

public class HomeController {
    private HomePanel view;

    public HomeController(HomePanel v) {
        this.view = v;
    }

    public void addPressed() {}

    public void editPressed() {
       view.getFrame().setSettingsPanel();
    }
}
