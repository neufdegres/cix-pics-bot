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

names = ['cix', 'bx', 'seunghun', 'yonghee', 'bae jinyoung', 'hyunsuk']
tags = ["#BX #승훈 #배진영 #용희 #현석", "#BX #이병곤 #병곤 #BYOUNGGON", "#승훈 #김승훈 #SEUNGHUN",
        "#용희 #김용희 #YONGHEE", "#배진영 #BAEJINYOUNG",
        "#현석 #윤현석 #HYUNSUK"]

def getPic(member):
    if(member == None): 
        randPic = bdd.getRandImg();
        pic = randPic[0]
        member = randPic[1]
    else : 
        pic = bdd.getImg(member)
        
    return [member, pic]

def getGif(member):
    """ 
    0: numero du membre
    1: lien du gif
    2: username du gifeur
    3: liste des booleens des hashtags
    """
    if(member == 0): member = None
    if(member == None): acc = bdd.getGifAccUser(None)
    else: acc = bdd.getGifAccUser(member)
    link = gifs.getRandomGif(acc, member)
    return [member, link[0], link[1], link[2]]

def replyStatus(update, inReplyTo, media):
    api.PostUpdate(update, media=media, in_reply_to_status_id=inReplyTo)

def getCommande(texte):
    global hello
    if(texte.startswith("RT @cixpicsbot:")): return None
    if(("give me a pic" in texte.lower()) 
        or ("give me a picture" in texte.lower())
        or ("give me a photo" in texte.lower())): return "pic"
    if("give me a gif" in texte.lower()): return "gif"
    if("hello @cixpicsbot" in texte.lower()): 
        choix = ["pic", "gif"]
        nbr = random.randint(0, 1)
        hello = True
        return choix[nbr]

def search(research, howMany):
    searchResults = api.GetSearch(raw_query="q="+research+"&result_type=recent&count="+howMany)
    for search in searchResults:
        if(not bdd.dejaRepondu(search.id)):
            bdd.newMention(search.id)
            cmd = getCommande(search.text)
            if(cmd != None): sendReply(search, cmd)

def sendReply(search, cmd):
    global tweets
    try:
        if(cmd == "pic"): replyPic(search)
        elif(cmd == "gif"): replyGif(search)
        print("Un tweet a bien été envoyé à @" + search.user.screen_name + " ! (" + str(tweets+1) + ")")
        tweets += 1
        if (tweets % 30 == 0): alert.statut(tweets)
        time.sleep(5)
    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])

def replyPic(search):
    global hello
    global names
    global tags
    pic = getPic(bdd.findMember(search.text))
    try:
        if(hello):
            replyStatus("@" + search.user.screen_name + " hello @" + search.user.screen_name +
                        " ! have a nice day <3\n\n#CIX #씨아이엑스 " +
                        tags[pic[0]], search.id, media=pic[1])
        else:
            replyStatus("@" + search.user.screen_name + " hi, here is a pic of " + names[pic[0]]
                        + " :) have a nice day <3\n\n#CIX #씨아이엑스 " + tags[pic[0]], search.id, media=pic[1])
    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])

def replyGif(search):
    global names
    global tags
    global hello
    gif = getGif(bdd.findMember(search.text))
    try:
        if(hello):
            replyStatus("@" + search.user.screen_name + " hello @" + search.user.screen_name + 
                        " ! have a nice day <3\n\n (cr to: @/" + gif[2] 
                        + ")\n#CIX #씨아이엑스 "+ getTags(gif[3]) + "\n" + gif[1],
                        search.id, media=None)
        else:
            if(gif[0] == None): 
                form = "your gif"
                tagline = getTags(gif[3])
            else: 
                form = "a gif of "  + names[gif[0]]
                tagline = tags[gif[0]]
            replyStatus("@" + search.user.screen_name + " hi, here is " + form
                        + " :) have a nice day <3\n\n(cr to: @/" + gif[2] + ")\n#CIX #씨아이엑스 "
                        + tagline + "\n" + gif[1], search.id, media=None)
    except:
        print(traceback.format_exc())
        alert.error(sys.exc_info()[1])

def getTags(membres):
    global tags
    res = ""
    a = 1
    for pers in membres[1:]:
        if(pers): res += tags[a] + " "
        a+=1
    if(res == ""): res += tags[0]
    return res

def start():
    global tweets
    stop = False
    err = None
    alert.updateDN(True)
    while(not stop):
        try:
            search("to%3Acixpicsbot OR %40cixpicsbot -from%3Acixpicsbot","5")
            time.sleep(15) 
        except:
            print(traceback.format_exc())
            err = sys.exc_info()[1]
            stop = True  
    alert.error(err)

start()