package database;

import java.sql.*;
import java.util.LinkedHashMap;
import java.util.LinkedList;

public class Functions {

    public static LinkedHashMap<Integer, String> getMembersFromDB() {
        LinkedHashMap<Integer, String> res = new LinkedHashMap<>();
        String query = "SELECT * FROM members";
        try(Connection con = DriverManager.getConnection(MySQL.DB_URL, MySQL.USER, MySQL.PASS);
            Statement stmt = con.createStatement();
            ResultSet rs = stmt.executeQuery(query)) {
                while (rs.next()) {
                    res.put(rs.getInt("id"), rs.getString("member"));            
                }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return res;
    }

    public static LinkedHashMap<Integer, String> getErasFromDB() {
        LinkedHashMap<Integer, String> res = new LinkedHashMap<>();
        String query = "SELECT * FROM eras";
        try(Connection con = DriverManager.getConnection(MySQL.DB_URL, MySQL.USER, MySQL.PASS);
            Statement stmt = con.createStatement();
            ResultSet rs = stmt.executeQuery(query)) {
                while (rs.next()) {
                    res.put(rs.getInt("id"), rs.getString("name"));     
                }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return res;
    }

    public static LinkedList<Pic> getPicsFromDB(String member, String era) {
        LinkedList<Pic> res = new LinkedList<>();
        String query = "";
        if(!member.isBlank()) {
            if(!era.isBlank()) {
                query = "SELECT pics.* FROM pics, members, eras"
                    + "  WHERE (members.member = \"" + member + "\" AND members.id = pics.id_member)"
                    + " AND (eras.name = \"" + era + "\" AND eras.id = pics.idEra);";
            } else {
                query = "SELECT pics.* FROM pics, members"
                    + "  WHERE (members.member = \"" + member + "\" AND members.id = pics.id_member);";
            }
        } else {
            if(!era.isBlank()) {
                query = "SELECT pics.* FROM pics, eras"
                    + " WHERE (eras.name = \"" + era + "\" AND eras.id = pics.idEra);";
            } else {
                query = "SELECT * FROM pics WHERE id%100=0+5";
            }
        }
        try(Connection con = DriverManager.getConnection(MySQL.DB_URL, MySQL.USER, MySQL.PASS);
            Statement stmt = con.createStatement();
            ResultSet rs = stmt.executeQuery(query)) {
                while(rs.next()) { 
                    res.add(new Pic(
                        rs.getInt("id"),
                        getMembersFromDB().get(rs.getInt("id_member")),
                        getNewPath(rs.getString("link")),
                        getErasFromDB().get(rs.getInt("idEra"))
                    ));
                    System.out.println("done ! [" + rs.getInt("id") + "]");
                }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return res;
    }

    public static void setEraToPic(Pic pic, String newEra) {
        int idEra = 0;
        if(!newEra.isBlank()) idEra = getKeyFromValue(getErasFromDB(), newEra);
        String query = "UPDATE pics SET idEra=" + idEra + " WHERE id=" + pic.getId() + ";";
        try(Connection con = DriverManager.getConnection(MySQL.DB_URL, MySQL.USER, MySQL.PASS);
            Statement stmt = con.createStatement();) {
                stmt.executeUpdate(query);
                pic.setEra(newEra);
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    private static String getNewPath(String org) {
        String res = "/home/vicky/Projets/twitterBots/Picturebot/PICS/";
        res += org.substring(30);
        System.out.println(res);
        return res;
    }

    private static int getKeyFromValue(LinkedHashMap<Integer, String> map, String value) {
        for(var entry : map.entrySet()) {
            if(entry.getValue().equals(value)) return entry.getKey();
        }
        return 0;
    }

}
