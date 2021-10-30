import interactions_bdd as bdd
from config import getApi

api = getApi()

def printSearch(liste):
    for tweet in liste:
        print("posté à " + tweet.created_at + " par @" + tweet.user.screen_name + " (" + str(tweet.id) + ")\n\'" + tweet.text + "\'\n")

def searchTest():
    results = api.GetSearch(raw_query="q=to%3Acixpicsbot OR %40cixpicsbot -from%3Acixpicsbot&result_type=recent&count=50")
    printSearch(results)

def tweetTest(update, media, inReplyTo):
    api.PostUpdate(update, media=media, in_reply_to_status_id=inReplyTo)

# first = numero de la premiere image non mise
# last = numero de la dernière image non mise

# bdd.inserer(1,86,1)
# bdd.inserer(1,127,2)
# bdd.inserer(1,104,3)
# bdd.inserer(1,97,4)
# bdd.inserer(1,101,5)

# bdd.remplissage()

# bdd.remplissageAux()

# searchTest()

# tweetTest("yo", "/home/ubuntu/picture_bot/pics/2/55.jpg", None)