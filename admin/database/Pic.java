package database;

public class Pic {
    private int id;
    private String member; // in String !! [ex : seunghun]
    private String path;
    private String era; // idem !! [ex : jungle]

    public Pic(int i, String m, String p, String e) {
        this.id = i;
        this.member = m;
        this.path = p;
        this.era = e;
    }

    public int getId() {
        return id;
    }

    public String getMember() {
        return member;
    }

    public String getPath() {
        return path;
    }

    public String getEra() {
        return era;
    }

    public void setEra(String newEra) {
        this.era = newEra;
    }
}
