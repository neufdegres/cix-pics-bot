from config import getApi
import interactions_bdd as bdd
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
        1 : {"name" : "bx", "tags" : "#BX #이병곤 #병곤 #BYOUNGGON"},
        2 : {"name" : "seunghun", "tags" : "#승훈 #김승훈 #SEUNGHUN"},
        3 : {"name" : "yonghee", "tags" : "#용희 #김용희 #YONGHEE"},
        4 : {"name" : "bae jinyoung", "tags" : "#배진영 #BAEJINYOUNG"},
        5 : {"name" : "hyunsuk", "tags" : "#현석 #윤현석 #HYUNSUK"},
        12 : {"name" : "gonhun", "tags" : "#BX #승훈"},
        13 : {"name" : "gonhee", "tags" : "#BX #배진영"},
        14 : {"name" : "gonbae", "tags" : "#BX #용희"},
        15 : {"name" : "gonsuk", "tags" : "#BX #현석"},
        23 : {"name" : "hunhee", "tags" : "#승훈 #용희"},
        24 : {"name" : "baehun", "tags" : "#승훈 #배진영"},
        25 : {"name" : "seunghyun", "tags" : "#승훈 #현석"},
        34 : {"name" : "yongbae", "tags" : "#용희 #배진영"},
        35 : {"name" : "yongsuk", "tags" : "#용희 #현석"},
        45 : {"name" : "yoonbae", "tags" : "#배진영 #현석"}
    }
    return member[id];

def get_pic(member):
    if(member == None): 
        randPic = bdd.getRandImg();
        pic = randPic[0]
        member = randPic[1]
    else : 
        pic = bdd.getImg(member)
        
    # return [member, pic]
    return {"member_id" : member, "link" : pic}

def get_gif(member):
    """ 
    return {"member_id", "link", "user", "tags"}
    """
    if(member == 0): member = None
    max_tries = 5
    while(max_tries > 0) :
        try :
            if(member == None): acc = bdd.getGifAccUser(None)
            else: acc = bdd.getGifAccUser(member)
            link = gifs.getRandomGif(acc, member)
            return {"member_id" : member, "link" : link[0], "user" : link[1], "tags" : link[2]}
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

def search(research, howMany):
    searchResults = api.GetSearch(raw_query="q="+research+"&result_type=recent&count="+howMany)
    for search in searchResults:
        if(not bdd.dejaRepondu(search.id)):
            cmd = get_commande(search.text)
            if(cmd != None): send_reply(search, cmd)
            bdd.newMention(search.id)

def send_reply(search, cmd):
    global tweets
    try:
        if(cmd == "pic"): reply_pic(search)
        elif(cmd == "gif"): reply_gif(search)
        print("Un tweet a bien été envoyé à @" + search.user.screen_name + " ! (" + str(tweets+1) + ")")
        tweets += 1
        if (tweets % 30 == 0): alert.statut(tweets)
        time.sleep(5)
    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])

def reply_pic(search):
    global hello
    global names
    global tags
    pic = get_pic(bdd.findMember(search.text))
    try:
        strings = get_strings(pic["member_id"])
        if(hello):
            reply_status("@" + search.user.screen_name + " hello @" + search.user.screen_name +
                        " ! have a nice day <3\n\n#CIX #씨아이엑스 " +
                        strings["tags"], search.id, media=pic["link"])
        else:
            reply_status("@" + search.user.screen_name + " hi, here is a pic of " + strings["name"]
                        + " :) have a nice day <3\n\n#CIX #씨아이엑스 " + strings["tags"],
                        search.id, media=pic["link"])
    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])
     
def reply_gif(search):
    global names
    global tags
    global hello
    gif = get_gif(bdd.findMember(search.text))
    try:
        if(hello):
            reply_status("@" + search.user.screen_name + " hello @" + search.user.screen_name + 
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
            reply_status("@" + search.user.screen_name + " hi, here is " + form
                        + " :) have a nice day <3\n\n(cr to: @/" + gif["user"] + ")\n#CIX #씨아이엑스 "
                        + tagline + "\n" + gif["link"], search.id, media=None)
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
    stop = False
    err = None
    alert.updateDN(True)
    while(not stop):
        try:
            search("to%3Acixpicsbot OR %40cixpicsbot -from%3Acixpicsbot","5")
            if (hello) : hello = False
            time.sleep(15) 
        except:
            print(traceback.format_exc())
            err = sys.exc_info()[1]
            stop = True  
    alert.error(err)

start()