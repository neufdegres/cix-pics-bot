# import interactions_bdd as bdd
from config import getApi

api = getApi()

def printSearch(liste):
    for tweet in liste:
        print(tweet)
        # print(tweet.media)
        # print("posté à " + tweet.created_at + " par @" + tweet.user.screen_name + " (" + str(tweet.id) + ")\n\'" + tweet.text + "\'\n")

def searchTest():
    # results = api.GetSearch(raw_query="q=to%3Acixpicsbot OR %40cixpicsbot -from%3Acixpicsbot&result_type=recent&count=50")
    results = api.GetStatus(1339420052433584130)
    # results = api.GetUserTimeline(screen_name="cixpicsbot", include_rts=False, count=1)
    # if(len(results)!=0): print("aie")
    return results
    # print(len(results))
    # printSearch(results)

def tweetTest(update, media, inReplyTo):
    api.PostUpdate(update, media=media, in_reply_to_status_id=inReplyTo)

    
def getHashtags(tweet):
    liste = []
    membres = [False, False, False, False, False, False]
    i=0
    while(i < len(tweet.hashtags)):
        liste.append(tweet.hashtags[i].text)
        i+=1
    # determiner qui sont dans ces hashtag
    for name in liste:
        if(name.lower() == "cix"): membres[0] = True
        elif(name.lower() == "bx" or "병곤" in name): membres[1] = True
        elif("승훈" in name or name.lower() == "seunghun"): membres[2] = True
        elif("용희" in name or name.lower() == "yonghee"): membres[3] = True
        elif("배진영" in name or name.lower() == "baejinyoung"): membres[4] = True
        elif("현석" in name or name.lower() == "hyunsuk"): membres[5] = True
    return membres

tags = ["#BX #승훈 #배진영 #용희 #현석", "#BX #이병곤 #병곤 #BYOUNGGON", "#승훈 #김승훈 #SEUNGHUN",
        "#용희 #김용희 #YONGHEE", "#배진영 #BAEJINYOUNG",
        "#현석 #윤현석 #HYUNSUK"]

def getTags(membres):
    global tags
    res = ""
    a = 1
    for pers in membres[1:6]:
        if(pers): res += tags[a] + " "
        a+=1
    if(res == ""): res += tags[0]
    return res

# first = numero de la premiere image non mise
# last = numero de la dernière image non mise

# bdd.inserer(1,91,0)
# bdd.inserer(87,239,1)
# bdd.inserer(128,304,2)
# bdd.inserer(105,288,3)
# bdd.inserer(98,259,4)
# bdd.inserer(102,213,5)

# bdd.remplissage()

# bdd.remplissageAux()

res = getHashtags(searchTest())

print(getTags(res))

# if(len(res) == 0): print("erreur")
# for t in res :
#     print(str(t)," ")

# tweetTest("yo", "/home/ubuntu/picture_bot/pics/2/55.jpg", None)