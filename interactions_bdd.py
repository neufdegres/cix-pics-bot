import os
from config import getApi
import alert
import mysql.connector as MC
import sys
import traceback

api = getApi()

try:
    conn = MC.connect(host = 'localhost', database = 'picture_bot', user = 'root', password = '#@BOT77degres')
    cursor = conn.cursor()

except MC.Error as err:
    alert.error(err)

def deconnexion():
    global cursor
    global conn
    if(conn.is_connected()):
        cursor.close()
        conn.close()

def inserer(first, last, member): # update la base de donnnés
    while(first<=last) : # last = numero de la dernière image non mise
        req = 'INSERT INTO pics(link,idMember) VALUES(%s, %s)'
        infos = ("/home/ubuntu/picture_bot/pics/" + str(member) + "/" + str(first) + ".jpg", member)

        cursor.execute(req, infos)
        conn.commit()

        first+=1

    print("Fini !")

def getImg(member):
    try:
        req = "SELECT * FROM pics WHERE idMember=" + str(member)+ " ORDER BY RAND()"
        cursor.execute(req)

        results = cursor.fetchall()

        while(True):
            for line in results:
                return line[1]

    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])
        
def getRandImg():
    try:
        req = "SELECT * FROM pics ORDER BY RAND()"
        cursor.execute(req)

        results = cursor.fetchall()

        while(True):
            for line in results:
                return [line[1], line[2]] # A MODIFIER !! (ORDRE DES COLONES)

    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])

def findMember(textBrut):
    text = deleteAtUser(textBrut)
    try:
        req = "SELECT * FROM designations;"
        cursor.execute(req)

        results = cursor.fetchall()

        for name in results:
            if(name[1] in text.lower()):
                return name[2]
        return None

    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])

def find_era(textBrut): # pas encore implémenté
    text = deleteAtUser(textBrut)
    try:
        req = "SELECT * FROM eras;"
        cursor.execute(req)
        
        results = cursor.fetchall()
        
        for era in results:
            if(era[1] in text.lower()):
                return era[0] # id de l'era
        return None
    
    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])        

def deleteAtUser(text):
    # string to char[]
    cList = [char for char in text]
    a = 0
    for c in cList:
        if(c == '@'):
            while(a+1 != len(cList) and cList[a+1] != ' '):
                del cList[a+1]
        a+=1
    str1 = ""
    return str1.join(cList) # char[] to string

def remplissageAux():
    results = api.GetSearch(raw_query="q=to%3Acixpicsbot OR %40cixpicsbot -from%3Acixpicsbot&result_type=recent&count=50")
    try:
        for tweet in results:
            req = 'INSERT INTO mentions(tweet) VALUES('+str(tweet.id)+');'
            # infos = 
            cursor.execute(req)
            conn.commit()

        print("Fait !")
    
    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])

def dejaRepondu(tweetID):
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

def newMention(tweetID):
    try:
        req = 'INSERT INTO mentions(tweet) VALUES('+str(tweetID)+');'
        cursor.execute(req)
        conn.commit()

    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])
        
def getGifAccUser(member):
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
        
def get_count_member_pics(id_member):
    try:
        req = "SELECT * FROM pics WHERE idMember="+ str(id_member) + ";"
        cursor.execute(req)
        
        results = cursor.fetchall()
        
        return len(results)
    
    except:
        print(traceback.format_exc())
     
def get_last_pic_to_add(id_member):
    dossiers = os.listdir('./PICS/' + str(id_member))
    return len(dossiers)
            
def update_database():
    # inserer(get_count_member_pics(0)+1, get_last_pic_to_add(0), 0)
    inserer(get_count_member_pics(1)+1, get_last_pic_to_add(1), 1)
    inserer(get_count_member_pics(2)+1, get_last_pic_to_add(2), 2)
    inserer(get_count_member_pics(3)+1, get_last_pic_to_add(3), 3)
    inserer(get_count_member_pics(4)+1, get_last_pic_to_add(4), 4)
    inserer(get_count_member_pics(5)+1, get_last_pic_to_add(5), 5)