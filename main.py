from datetime import datetime, timedelta, timezone
from config import getApi
import db_interaction as db
import gifs
import alert
import sys
import time
import random
import traceback

# le bot envoie au maximum 5 tweets à la fois, toutes les 15 secondes

api = getApi()

tweets = 0
hello = False

def get_strings(id):
    member = {
        0 : {"name" : "cix", "tags" : "#BX #승훈 #배진영 #용희 #현석"},
        1 : {"name" : "bx", "tags" : "#BX #이병곤 #BYOUNGGON"},
        2 : {"name" : "seunghun", "tags" : "#승훈 #김승훈 #SEUNGHUN"},
        3 : {"name" : "yonghee", "tags" : "#용희 #김용희 #YONGHEE"},
        4 : {"name" : "bae jinyoung", "tags" : "#배진영 #BAEJINYOUNG"},
        5 : {"name" : "hyunsuk", "tags" : "#현석 #윤현석 #HYUNSUK"},
        12 : {"name" : "gonhun", "tags" : "#BX #이병곤 #승훈 #SEUNGHUN"},
        13 : {"name" : "gonhee", "tags" : "#BX #이병곤 #용희 #YONGHEE"},
        14 : {"name" : "gonbae", "tags" : "#BX #이병곤 #배진영 #BAEJINYOUNG"},
        15 : {"name" : "gonsuk", "tags" : "#BX #이병곤 #현석 #HYUNSUK"},
        23 : {"name" : "hunhee", "tags" : "#승훈 #SEUNGHUN #용희 #YONGHEE"},
        24 : {"name" : "baehun", "tags" : "#승훈 #SEUNGHUN #배진영 #BAEJINYOUNG"},
        25 : {"name" : "seunghyun", "tags" : "#승훈 #SEUNGHUN #현석 #HYUNSUK"},
        34 : {"name" : "yongbae", "tags" : "#용희 #YONGHEE #배진영 #BAEJINYOUNG"},
        35 : {"name" : "yongsuk", "tags" : "#용희 #YONGHEE #현석 #HYUNSUK"},
        45 : {"name" : "yoonbae", "tags" : "#배진영 #BAEJINYOUNG #현석 #HYUNSUK"}
    }
    return member[id]

def get_pic(member, era, option):
    """ 
    return {"id", "member_id", "link", "as_asked"}
    """
    is_member = True if member != None else False
    is_era = True if era != None else False
    as_asked = True
    attemp = 1 # max = 3 attemps 
    while(True):
        res = db.get_pic_from_db(member, era, option);
        if res != None : break
        as_asked = False
        if attemp == 1 :
            if is_era :
                era = None
                is_era = False
            elif is_member and not is_era :
                member = None
                is_member = False
            else :
                alert.error("Erreur lors de la selection de la photo dans la db.")
        elif attemp == 2 :
            if is_member and not is_era :
                member = None
                is_member = False
            else :
                alert.error("Erreur lors de la selection de la photo dans la db.")
        else :
                alert.error("Erreur lors de la selection de la photo dans la db.") 
    id = res["id"]      
    link = res["link"]
    if member == None : member = res["member_id"]
    return {"id" : id, "member_id" : member, "link" : link, "as_asked" : as_asked}

def get_gif(member):
    """ 
    return {"member_id", "link", "user", "tags", "origine"}
    """
    if member == 0 : member = None
    if member != None and member > 5 : member = None
    max_tries = 5
    while(max_tries > 0) :
        try :
            if(member == None): acc = db.get_gif_acc_user(None)
            else: acc = db.get_gif_acc_user(member)
            link = gifs.get_random_gif(acc, member)
            return {"member_id" : member, "link" : link[0], "user" : link[1], "tags" : link[2], "origine" : link[3]}
        except :
            max_tries -= 1

def reply_status(update, inReplyTo, media):
    api.PostUpdate(update, media=media, in_reply_to_status_id=inReplyTo)

def get_commande(texte):
    global hello
    if(texte.startswith("RT @cixpicsbot:")): return None
    elif(("give me a pic" in texte.lower()) 
        or ("give me a picture" in texte.lower())
        or ("give me a photo" in texte.lower())): return "pic"
    elif("give me a gif" in texte.lower()): return "gif"
    elif("hello @cixpicsbot" in texte.lower()): 
        choix = ["pic", "gif"]
        nbr = random.randint(0, 1)
        hello = True
        return choix[nbr]

def search(research):
    searchResults = api.GetSearch(raw_query="q="+research+"&result_type=recent&count=5")
    for search in searchResults:
        if(not db.deja_repondu(search.id)):
            cmd = get_commande(search.text)
            if(cmd != None): send_reply(search, cmd)
            db.new_mention(search.id)

def send_reply(search, cmd):
    global tweets
    try:
        if(cmd == "pic"): reply_pic(search)
        elif(cmd == "gif"): reply_gif(search)
        tweets += 1
        if (tweets % 30 == 0): alert.statut(tweets)
        time.sleep(5)
    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])

def delete_at_user(tweet):
    tab = tweet.split(" ")
    i = 0
    while(True):
        if i >= len(tab): break
        if tab[i].startswith("@"):
            del tab[i]
            continue
        i+=1
    return " ".join(tab)

def get_time():
    timezone_offset = 2.0 # to change when we'll pass to 1.0
    tzinfo = timezone(timedelta(hours=timezone_offset))
    return datetime.now(tzinfo)    

def reply_pic(search):
    global hello
    tweet = delete_at_user(search.text)
    member_id = db.find_member(tweet)
    era = db.find_era(tweet)
    # option = db.find_option(tweet)
    pic = get_pic(member_id, era["id"], None)
    try:
        now = get_time()
        time = now.strftime("%H:%M-%d/%m")
        strings = get_strings(pic["member_id"])
        username = search.user.screen_name
        if(hello):
            reply = "@" + username + " hello " + username + \
                        " ! have a nice day <3\n\n#CIX #씨아이엑스 " + strings["tags"]
        else :
            if pic["as_asked"]:
                reply = "@" + username + " hi, here is a pic of " + strings["name"]
                if era["name"] != None : reply += " from " + era["name"] + " era"
                reply += " :) have a nice day <3\n\n#CIX #씨아이엑스 " + strings["tags"]
            else :
                reply = "@" + username + " sorry, i couldn't answer your request :( here is a pic of " \
                    + strings["name"] + " anyway :)\n\n#CIX #씨아이엑스 " + strings["tags"]
        reply_status(reply, search.id, media=pic["link"])
        print("(" + str(tweets+1) + ") à " + username + " (pic #" + pic["id"] + ") " + time)
    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])
     
def reply_gif(search):
    global hello
    tweet = delete_at_user(search.text)
    gif = get_gif(db.find_member(tweet))
    try:
        now = get_time()
        time = now.strftime("%H:%M - %d/%m")
        username = search.user.screen_name
        if(hello):
            reply_status("@" + username + " hello " + username + 
                        " ! have a nice day <3\n\n (cr to: @/" + gif["user"] 
                        + ")\n#CIX #씨아이엑스 "+ get_tags_gif(gif["tags"]) + "\n" + gif["link"],
                        search.id, media=None)
        else:
            if(gif["member_id"] == None): 
                form = "your gif"
                tagline = get_tags_gif(gif["tags"])
            else: 
                strings = get_strings(gif["member_id"])
                form = "a gif of "  + strings["name"]
                tagline = strings["tags"]
            reply_status("@" + username + " hi, here is " + form
                        + " :) have a nice day <3\n\n(cr to: @/" + gif["user"] + ")\n#CIX #씨아이엑스 "
                        + tagline + "\n" + gif["link"], search.id, media=None)
        print("(" + str(tweets+1) + ") à " + username + " (gif " + gif["origine"] + ") " + time)
    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])

def get_tags_gif(membres):
    tags = ["#BX #승훈 #배진영 #용희 #현석", "#BX #이병곤 #BYOUNGGON", "#승훈 #김승훈 #SEUNGHUN",
        "#용희 #김용희 #YONGHEE", "#배진영 #BAEJINYOUNG",
        "#현석 #윤현석 #HYUNSUK"]
    res = ""
    a = 1
    for pers in membres[1:]:
        if(pers): res += tags[a] + " "
        a+=1
    if(res == ""): res += tags[0]
    return res

def start():
    global tweets
    global hello
    err = None
    alert.updateDN(True)
    while(True):
        try:
            search("to%3Acixpicsbot OR %40cixpicsbot -from%3Acixpicsbot")
            if hello : hello = False
            time.sleep(15) 
        except:
            print(traceback.format_exc())
            err = sys.exc_info()[1]
            break  
    alert.error(err)

start()