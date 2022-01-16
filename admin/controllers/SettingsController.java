package controllers;

import views.SettingsPanel;

public class SettingsController {
    private SettingsPanel vue;

    public SettingsController(SettingsPanel v) {
        this.vue = v;
    }

    public void confirmPressed() {
        var member = (String)vue.getMemberBox().getSelectedItem();
        var era = (String)vue.getEraBox().getSelectedItem();
        vue.getFrame().setEditPanel(member, era);
    }

    public void backPressed() {
        vue.getFrame().setHomePanel();
    }
}
