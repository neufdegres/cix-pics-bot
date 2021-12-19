from config import getApi
import interactions_bdd as bdd
import random
import sys
import time
import alert

api = getApi()

tags = ["#BX #승훈 #배진영 #용희 #현석", "#BX #이병곤 #병곤 #BYOUNGGON", "#승훈 #김승훈 #SEUNGHUN",
        "#용희 #김용희 #YONGHEE", "#배진영 #BAEJINYOUNG",
        "#현석 #윤현석 #HYUNSUK"]

def tweet(update, media) :
    api.PostUpdate(update, media=media)

def getPic():
    member = random.randint(0, 5)
    pic = bdd.getImg(member)
    return [member, pic]

def main():
    while(True):
        pic = getPic()
        try:
            tweet("#CIX #씨아이엑스 " + tags[pic[0]], media=pic[1])
            time.sleep(60*60)
        except:
            alert.error(sys.exc_info()[1])

