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
    res["member"] = db.find_member(texte)
    res["era"] = db.find_era(texte) # return {"id","name"}
    if not is_command(res): return None
    return res