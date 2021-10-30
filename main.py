from config import getApi
import interactions_bdd as bdd
import alert
import sys
import time
import random

# le bot envoie au maximum 5 tweets à la fois, toutes les 15 secondes

api = getApi()

tweets = 0

names = ['bx', 'seunghun', 'yonghee', 'bae jinyoung', 'hyunsuk']
tags = ["#BX #이병곤 #병곤 #BYOUNGGON", "#승훈 #김승훈 #SEUNGHUN",
        "#용희 #김용희 #YONGHEE", "#배진영 #BAEJINYOUNG",
        "#현석 #윤현석 #HYUNSUK"]

def getPic(member):
    if(member == None): member = random.randint(1, 5)
    pic = bdd.getImg(member)
    return [member-1, pic]

def replyStatus(update, inReplyTo, media):
    api.PostUpdate(update, media=media, in_reply_to_status_id=inReplyTo)

def peutRepondre(texte):
    if(texte.startswith("RT @cixpicsbot:")): return False
    elif("give me a pic" in texte.lower()): return True
    elif("give a pic" in texte.lower()): return True
    return False

def search(research, howMany):
    global tweets
    global names
    global tags
    searchResults = api.GetSearch(raw_query="q="+research+"&result_type=recent&count="+howMany)
    for search in searchResults:
        if(not bdd.dejaRepondu(search.id)):
            bdd.newMention(search.id)
            if(peutRepondre(search.text)):
                pic = getPic(bdd.findMember(search.text))
                try:
                    replyStatus("@" + search.user.screen_name + " hi, here is a pic of " + names[pic[0]]
                                + " :) have a nice day <3\n\n#CIX #씨아이엑스 " + tags[pic[0]], search.id, media=pic[1])
                    print("Un tweet a bien été envoyé à @" + search.user.screen_name + " ! (" + str(tweets+1) + ")")
                    tweets += 1
                    if (tweets % 30 == 0): alert.statut(tweets)
                    time.sleep(5)
                except:
                    alert.error(sys.exc_info()[1])

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
            err = sys.exc_info()[1]
            stop = True  
    alert.error(err)

start()