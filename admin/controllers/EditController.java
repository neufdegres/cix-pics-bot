package controllers;

import database.Functions;
import models.EditModel;
import views.EditPanel;

public class EditController {
    private EditPanel view;
    private EditModel model;

    public EditController(EditPanel v, EditModel m) {
        this.view = v;
        this.model = m;
    }

    public void editPressed() {
        String newEra = (String) view.getEraBox().getSelectedItem();
        Functions.setEraToPic(model.getActual(), newEra);
        view.updatePanel();
    }

    public void backPressed() {
        model.setBack();
        view.updatePanel();
    }

    public void nextPressed() {
        model.setNext();
        view.updatePanel();
    }

    public void goSettingsPressed() {
        view.getFrame().setSettingsPanel();
    }

}
