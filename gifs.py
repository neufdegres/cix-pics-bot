from random import randint
from config import getApi
import interactions_bdd as bdd

api = getApi()

# récupérer les 50 derniers gifs d'un user 
# récupérer le nom de la personne dans le tweet
# récupérer le media :
    # récuperer l'id du tweet
    # tweeter le DEUXIEME LIEN !!

''' 
1. chercher le nom de la personne demandée
2. chercher un compte gif qui poste des gif de ce membre
    si None, donner un compte au hasard
3. trouver un gif au hasard parmi les 50 derniers postés par le compte
4. verifier si le gif est bon (bonne personne/pas plusieur si spécifié)
5. retourner le numero du membre avec le lien du gif (9 si plusieurs personnes != 5)

'''

def getRandomGif(username, member):
    results = api.GetUserTimeline(screen_name=username, include_rts=False, count=100)
    valid = False
    while(True):
        n = randint(0,len(results)-1)
        tweet = results[n]
        if(isRightGif(tweet, member)): break
    return [getGifLink(tweet), username, getHashtags(tweet)]

def isRightGif(tweet, member):
    # si le tweet ne contient ni gif ni hashtag on renvoie False
    if(tweet.media == None): return False
    if(not("animated_gif" in str(tweet.media))): return False
    if(len(tweet.hashtags) == 0): return False
    tags = getHashtags(tweet)
    absent = 0
    for n in tags: 
        if(not n): absent+=1
    if(absent == 6): return False
    # on verifie mtn si on a reçu un gif du bon membre
    if(member != None):
        if(not (absent == 4 or absent == 5)): return False
        if(not tags[member]): return False
    return True
    
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

def getGifLink(tweet):
    line = str(tweet.media)
    # string to char[]
    cList = [char for char in line]
    # trouver une meilleure façon de faire...
    a = 0
    link = ""
    for c in cList:
        if(c == 'p' and cList[a+1] == 'i' and cList[a+2] == 'c'):
            # char[] to string
            link = link.join(cList[a:len(cList)-3])
            break
        a+=1
    return link
    