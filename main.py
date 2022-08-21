from datetime import datetime, timedelta, timezone
from config import getApi
import db_interaction as db
import parsing as ps
import os
import sys
import gifs
import alert
import time
import random
import traceback

# le bot envoie au maximum 5 tweets à la fois, toutes les 15 secondes

api = getApi()

tweets = 0

def get_time():
    timezone_offset = 2.0 # to change when we'll pass to 1.0
    tzinfo = timezone(timedelta(hours=timezone_offset))
    return datetime.now(tzinfo)    

def reply_status(update, inReplyTo, media):
    api.PostUpdate(update, media=media, in_reply_to_status_id=inReplyTo)

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

def search(research):
    searchResults = api.GetSearch(raw_query="q="+research+"&result_type=recent&count=5")
    for search in searchResults:
        if not db.deja_repondu(search.id) :
            cmd = ps.get_commande(search.text)
            print(cmd)
            if cmd != None : send_reply(search, cmd)
            db.new_mention(search.id)
        
def send_reply(tweet, cmd):
    global tweets
    try:
        if cmd["type"] == "stats" : reply_stats(tweet)
        if cmd["type"] == "pic" : reply_pic(tweet, cmd)
        if cmd["type"] == "gif" :
            if gifs.is_blamable(cmd):
                reply_pic(tweet, cmd)
            else:
                reply_gif(tweet, cmd)
        if cmd["type"] == None : reply_rand(tweet, cmd)
        tweets += 1
        if (tweets % 30 == 0): alert.statut(tweets)
        time.sleep(5)
    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])    

def reply_pic(tweet, cmd):
    hello = cmd["hello"]
    member_id = cmd["member"]
    era = cmd["era"]
    was_gif_asked = True if cmd["type"] == "gif" else False
    # option = cmd["option"]
    pic = get_pic(member_id, era["id"], None)
    try:
        now = get_time()
        time = now.strftime("%H:%M-%d/%m")
        strings = get_strings(pic["member_id"])
        username = tweet.user.screen_name
        if was_gif_asked :
            reply = "@" + username + " hi, unfortunally you can't ask for a gif with the option(s) "\
                    + "you asked... here is a pic anyway :)\n\n#CIX #씨아이엑스 " + strings["tags"]
        elif hello and pic["as_asked"] :
            reply = "@" + username + " hello " + username + \
                        " ! have a nice day <3\n\n#CIX #씨아이엑스 " + strings["tags"]
        else :
            if pic["as_asked"]:
                reply = "@" + username + " hi, here is a pic of " + strings["name"]
                if era["name"] != None : reply += " from " + era["name"] + " era"
                reply += " :)\n\n#CIX #씨아이엑스 " + strings["tags"]
            else :
                reply = "@" + username + " sorry, i couldn't answer your request... here is a pic of " \
                    + strings["name"] + " anyway :)\n\n#CIX #씨아이엑스 " + strings["tags"]
        reply_status(reply, tweet.id, media=pic["link"])
        db.update_replies(tweet.user.id)
        print("(" + str(tweets+1) + ") à " + username + " (pic #" + pic["id"] + ") " + time)
    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])

def reply_gif(tweet, cmd):
    hello = cmd["hello"]
    gif = get_gif(cmd["member"])
    try:
        now = get_time()
        time = now.strftime("%H:%M - %d/%m")
        username = tweet.user.screen_name
        if hello :
            reply_status("@" + username + " hello " + username + 
                        " ! have a nice day <3\n\n(cr to: @/" + gif["user"] 
                        + ")\n#CIX #씨아이엑스 "+ gifs.get_tags(gif["tags"]) + "\n" + gif["link"],
                        tweet.id, media=None)
        else:
            if gif["member_id"] == None : 
                form = "your gif"
                tagline = gifs.get_tags(gif["tags"])
            else: 
                strings = get_strings(gif["member_id"])
                form = "a gif of "  + strings["name"]
                tagline = strings["tags"]
            reply_status("@" + username + " hi, here is " + form
                        + " :)\n\n(cr to: @/" + gif["user"] + ")\n#CIX #씨아이엑스 "
                        + tagline + "\n" + gif["link"], tweet.id, media=None)
        db.update_replies(tweet.user.id)
        print("(" + str(tweets+1) + ") à " + username + " (gif " + gif["origine"] + ") " + time)
    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])

def reply_stats(tweet):
    try:
        now = get_time()
        time = now.strftime("%H:%M-%d/%m")
        username = tweet.user.screen_name
        count = db.get_user_count(tweet.user.id)
        end = " times." if count > 1 else " time."
        reply = "@" + username + " hi, you used this bot a total of " + str(count) + str(end)
        reply_status(reply, tweet.id, media=None)
        print("(" + str(tweets+1) + ") à " + username + " (stats) " + time)
    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])

def reply_rand(tweet, cmd):
    if ps.is_era(cmd) : reply_pic(tweet, cmd)
    elif cmd["member"] != None and (cmd["member"] == 0 or cmd["member"] > 5) : 
        reply_pic(tweet, cmd)
    else :
        nbr = random.randint(0, 1)
        if nbr == 0 : 
            reply_pic(tweet, cmd)
        else :
            reply_gif(tweet, cmd)

def start():
    global tweets
    err = None
    alert.updateDN(True)
    while(True):
        try:
            search("to%3Acixpicsbot OR %40cixpicsbot -from%3Acixpicsbot")
            time.sleep(15) 
        except:
            print(traceback.format_exc())
            err = sys.exc_info()[1]
            break  
    alert.error(err)

start()