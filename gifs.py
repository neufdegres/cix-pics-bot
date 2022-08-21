from random import randint
from config import getApi
from parsing import is_only_hello, is_era

api = getApi()

def get_random_gif(username, member):
    results = api.GetUserTimeline(screen_name=username, include_rts=False, count=200)
    while(True):
        n = randint(0,len(results)-1)
        tweet = results[n]
        origine = tweet.id_str
        if(is_right_gif(tweet, member)): break
    return [get_gif_link(tweet), username, get_hashtags_tweet(tweet), origine]

def is_right_gif(tweet, member):
    # si le tweet ne contient ni gif ni hashtag on renvoie False
    if(tweet.media == None): return False
    if(not("animated_gif" in str(tweet.media))): return False
    if(len(tweet.hashtags) == 0): return False
    tags = get_hashtags_tweet(tweet)
    absent = 0
    for n in tags: 
        if(not n): absent+=1
    if(absent == 6): return False
    # on verifie mtn si on a reçu un gif du bon membre
    if(member != None):
        if(not (absent == 4 or absent == 5)): return False
        if(not tags[member]): return False
    return True
    
def get_hashtags_tweet(tweet):
    liste = []
    membres = [False, False, False, False, False, False]
    i=0
    while(i < len(tweet.hashtags)):
        liste.append(tweet.hashtags[i].text)
        i+=1
    # on détermine qui sont dans ces hashtags
    for name in liste:
        if(name.lower() == "cix"): membres[0] = True
        elif(name.lower() == "bx" or "병곤" in name): membres[1] = True
        elif("승훈" in name or name.lower() == "seunghun"): membres[2] = True
        elif("용희" in name or name.lower() == "yonghee"): membres[3] = True
        elif("배진영" in name or name.lower() == "baejinyoung"): membres[4] = True
        elif("현석" in name or name.lower() == "hyunsuk"): membres[5] = True
    return membres

def get_gif_link(tweet):
    return tweet.media[0].display_url
    
def get_tags(membres):
    tags = ["#BX #승훈 #배진영 #용희 #현석", "#BX #이병곤 #BYOUNGGON", "#승훈 #김승훈 #SEUNGHUN",
        "#용희 #김용희 #YONGHEE", "#배진영 #BAEJINYOUNG",
        "#현석 #윤현석 #HYUNSUK"]
    res = ""
    a = 1
    for pers in membres[1:]:
        if(pers): res += tags[a] + " "
        a+=1
    if res == "" or len(res) == 5  : res = tags[0]
    return res

def is_blamable(cmd):
    if is_only_hello(cmd) : return False
    if cmd["member"] != None and (cmd["member"] == 0 or cmd["member"] > 5) : return True
    if is_era(cmd) : return True
    return False