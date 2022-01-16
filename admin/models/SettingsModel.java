package models;

import java.util.LinkedHashMap;

import database.Functions;

public class SettingsModel {
    private String[] members, eras;

    public SettingsModel() {
        this.members = mapToArray(Functions.getMembersFromDB());
        this.eras = mapToArray(Functions.getErasFromDB());
    }

    public String[] getMembers() {
        return members;
    }

    public String[] getEras() {
        return eras;
    }

    private String[] mapToArray(LinkedHashMap<Integer, String> map) {
        String[] res = new String[map.size() + 1];
        res[0] = " ";
        int a = 1;
        for(var entry : map.entrySet()) {
            res[a] = entry.getValue();
            a++;
        }
        return res;
    }
}
