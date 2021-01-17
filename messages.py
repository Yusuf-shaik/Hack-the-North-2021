import json
from datetime import datetime
from translate import translate_text, getLanguageList


def sendMessage(initialUser, text):

    now = datetime.now()
    time = now.strftime("%I:%M")
    

    languageFile = open("languages.json", "r")
    langDict = json.load(languageFile) 
    languageFile.close()

    translations = {}
    for a in langDict.values():
        translations[a] = translate_text(text, getLanguageList()[a])

    arr = [initialUser, translations, time]

    jsonFile = open("data.json", "r")
    data = json.load(jsonFile) 
    jsonFile.close()


    data.append(arr)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    


 

def getMessages():
    jsonFile = open("data.json", "r")
    data = json.load(jsonFile) 
    jsonFile.close()
    return data


    

