import os
import sys
import alert
import traceback
from config import getApi
import mysql.connector as MC

api = getApi()

try:
    conn = MC.connect(host = os.environ['host_local'],
                      database = os.environ['database_cpb'],
                      user = os.environ['user_local'],
                      password = os.environ['password_local'])
    
    cursor = conn.cursor()

except MC.Error as err:
    print(traceback.format_exc())
    alert.error(err)

def get_pic_from_db(member, era, option):
    member_str = era_str = option_str = where = and_1 = and_2 = ""
    
    if member != None : member_str = " idMember=" + str(member)
    if era != None : era_str = " idEra=" + str(era) 
    if option != None : option_str = " idOption=" + str(option) 
    
    if not member == era == option == None : where = " WHERE"
    if (member != None and era != None) or (member != None and option != None) \
        or (era != None and option != None) : and_1 = " AND"
    if (member != None) and (era != None) and (option != None) : and_2 = " AND"
        
    try:
        req = "SELECT * FROM pics" + where + member_str + and_1 + era_str \
            + and_2 + option_str + " ORDER BY RAND() LIMIT 1;"
        cursor.execute(req)

        results = cursor.fetchall()
        
        if len(results) == 0 : return None

        while(True):
            for line in results:
                return {"id": str(line[0]), "link" : line[1], "member_id" : line[2]}

    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])
    
def find_member(text):
    try:
        req = "SELECT * FROM designations;"
        cursor.execute(req)

        results = cursor.fetchall()
        
        tab = text.split(" ")

        for name in results:
            for word in tab :
                if name[1] in word.lower() :
                    return name[2] # member's id
        return None

    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])

def find_era(text):
    try:
        req = "SELECT * FROM eras;"
        cursor.execute(req)
        
        results = cursor.fetchall()
        
        for era in results:
            if(era[1] in text.lower()):
                return {"id" : era[0], "name" : era[1]}
        return {"id" : None, "name" : None}
    
    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])        

def find_option(text):
    return None

def deja_repondu(tweetID):
    try:
        req = "SELECT * FROM mentions;"
        cursor.execute(req)

        results = cursor.fetchall()

        for ligne in results:
            if(ligne[1] in str(tweetID)):
                return True
        return False

    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])

def new_mention(tweetID):
    try:
        req = 'INSERT INTO mentions(tweet) VALUES('+str(tweetID)+');'
        cursor.execute(req)
        conn.commit()

    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])
        
def get_gif_acc_user(member):
    try:
        if member == None:
            req = "SELECT username FROM gifs_accs ORDER BY RAND()"
        else:
            req = "SELECT gifs_accs.username FROM gifs_accs, members_gifs WHERE \
                    (gifs_accs.id = members_gifs.idAccount && members_gifs.idMember=" \
                    + str(member)+ ") ORDER BY RAND() "
        cursor.execute(req)

        results = cursor.fetchall()

        while(True):
            for line in results:
                return line[0]

    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])

def add_new_user(userID):
    try:
        req = 'INSERT INTO users_stats(user) VALUES('+str(userID)+');'
        cursor.execute(req)
        conn.commit()

    except:
        print(traceback.format_exc())
        
def update_user(userID, newcount):
    try:
        req = 'UPDATE users_stats SET count=' + str(newcount) + ' WHERE user=' + str(userID) + ';'
        cursor.execute(req)
        conn.commit()

    except:
        print(traceback.format_exc())
    
def get_user_count(userID):
    try:
        req = "SELECT count FROM users_stats WHERE user=" + str(userID) + ";"
        cursor.execute(req)

        results = cursor.fetchall()
        
        if len(results) == 0 : return 0

        for ligne in results:
            return int(ligne[0])
        
        return -1

    except:
        print(traceback.format_exc())
    
def update_replies(userID):
    if(userID == "1107350682716327936" or userID == "1374081770849759238"
                or userID == "1400947929653862401") : return
    count = get_user_count(userID)
    if count == 0:
        add_new_user(userID)
    else:
        update_user(userID, count+1)

# for updating the database

def inserer(first, last, member): # update la base de donnnés
    while(first<=last) : # last = numero de la dernière image non mise
        req = 'INSERT INTO pics(link,idMember) VALUES(%s, %s)'
        infos = ("/home/ubuntu/picture_bot/pics/" + str(member) + "/" + str(first) + ".jpg", member)

        cursor.execute(req, infos)
        conn.commit()

        first+=1

    print("Fini !")  
    
def get_count_member_pics(id_member):
    try:
        req = "SELECT * FROM pics WHERE idMember="+ str(id_member) + ";"
        cursor.execute(req)
        
        results = cursor.fetchall()
        
        return len(results)
    
    except:
        print(traceback.format_exc())
     
def get_last_pic_to_add(id_member):
    dossiers = os.listdir('./pics/' + str(id_member))
    return len(dossiers)
            
def update_database():
    cat = [0,1,2,3,4,5,12,13,14,15,23,24,25,34,35,45]
    for i in cat:   
        inserer(get_count_member_pics(i)+1, get_last_pic_to_add(i), i)