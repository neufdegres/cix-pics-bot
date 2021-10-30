from config import getApi
import sys

api = getApi()

def error(message):
    if (len(str(message)) < 1): message = "interruption par le terminal."
    api.PostDirectMessage("Le bot a été stoppé : " + str(message), user_id=1107350682716327936, screen_name="cixnemaa", return_json=False)
    updateDN(False)
    sys.exit(0)

def statut(nombre):
    api.PostDirectMessage(str(nombre) + " messages ont été envoyés depuis le lancement du bot.", user_id=1107350682716327936, screen_name="cixnemaa", return_json=False)

def updateDN(start):
    nName = api.GetUser(1400947929653862401).name
    if (start == True):
        if(nName.endswith("(off)")): 
            nName = nName.removesuffix(" (off)")
    else:
        if(not nName.endswith("(off)")):
            nName += (" (off)")
    api.UpdateProfile(name=nName)