package models;

import java.util.LinkedHashMap;
import java.util.LinkedList;

import database.Functions;
import database.Pic;

public class EditModel {
    private String[] eras;
    private LinkedList<Pic> pics;
    private Pic actual;
    private int actualIndex;

    public EditModel(String member, String era) {
        eras = mapToArray(Functions.getErasFromDB());
        pics = Functions.getPicsFromDB(member, era);
        if(pics.size() > 0) actual = pics.getFirst();
        else actual = null; 
        actualIndex = 0;       
    }

    public String[] getEras() {
        return eras;
    }

    public Pic getActual() {
        return actual;
    }

    public boolean isNext() {
        return !(actual == pics.getLast());
    }

    public boolean isBack() {
        return !(actual == pics.getFirst());
    }

    public void setBack() {
        if(isBack()) {
            actualIndex--;
            actual = pics.get(actualIndex);
        }
    }

    public void setNext() {
        if(isNext()) {
            actualIndex++;
            actual = pics.get(actualIndex);
        }
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
