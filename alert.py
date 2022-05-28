from config import getApi
import os
import sys

api = getApi()

def error(message):
    if (len(str(message)) < 1): message = "interruption par le terminal."
    api.PostDirectMessage("Le bot a été stoppé : " + str(message), user_id=os.environ['admin_id'], screen_name=os.environ['admin_at'], return_json=False)
    updateDN(False)
    sys.exit(0)

def statut(nombre):
    api.PostDirectMessage(str(nombre) + " messages ont été envoyés depuis le lancement du bot.", user_id=os.environ['admin_id'], screen_name=os.environ['admin_at'], return_json=False)

def updateDN(start):
    nName = api.GetUser(os.environ['cpb_id']).name
    if (start == True):
        if(nName.endswith("(off)")): 
            nName = nName.removesuffix(" (off)")
    else:
        if(not nName.endswith("(off)")):
            nName += (" (off)")
    api.UpdateProfile(name=nName)