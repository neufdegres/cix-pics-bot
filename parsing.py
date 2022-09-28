from random import choice
import db_interaction as db

def find_type(texte):
    tab = texte.split(" ")
    pics = ["pic", "picture", "photo", "image"]
    for mot in tab:
        if mot.lower() == "gif":
            return "gif"
        if mot.lower() in pics:
            return "pic"
    return None

def find_members(texte):
    tab = texte.split()
    members = []
    for word in tab:
        member = db.find_member(word)
        if member != None:
            members.append(member)
    if len(members) == 0 : return None
    if len(members) == 1 : return members[0]
    res = find_duo_trio(members)
    if res == None or res == "" : return -choice(members)
    return int(res)

def find_duo_trio(members):
    asked = {1:False, 2:False, 3:False, 4:False, 5:False}
    for m in members :
        if m > 0 and m <= 5:
            asked[m] = True
        else :
            return None
    res = ""
    for key, value in asked.items() :
        if value == True:
            res += str(key)
    return res

def delete_mentions(tweet):
    tab = tweet.split(" ")
    i = 0
    while(True):
        if i >= len(tab): break
        if "@cixpicsbot" in tab[i].lower() :
            tab[i] = "$at$"
        if tab[i].startswith("@") :
            del tab[i]
            continue
        i+=1
    return " ".join(tab)
    
def is_command(param):
    return param["hello"] == True or param["type"] != None
    
def is_only_hello(param):
    return (param["hello"] == True 
        and param["type"] == None 
        and param["member"] == None 
        and not is_era(param))  
    
def is_era(param):
    return  param["era"]["id"] != None and param["era"]["name"] != None
    
def get_commande(texte):
    global hello
    if texte.startswith("RT @cixpicsbot:") : return None
    res = {"hello": False, "type": None, "member": None, "era": None}
    texte = delete_mentions(texte)
    if texte.lower() == "stats $at$" or texte.lower() == "$at$ stats":
        res["type"] = "stats"
        return res
    if "hello $at$" in texte.lower() :
        res["hello"] = True
    res["type"] = find_type(texte)
    res["member"] = find_members(texte)
    res["era"] = db.find_era(texte) # return {"id","name"}
    if not is_command(res): return None
    return res