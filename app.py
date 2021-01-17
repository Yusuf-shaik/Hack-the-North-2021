from flask import Flask, render_template, redirect, url_for, request, session
from flask_apscheduler import APScheduler
import requests
from messages import sendMessage, getMessages
from translate import getLanguageList, translate_text
import json
import time


app = Flask(__name__)

app.secret_key = "bonjour"



@app.route('/') 
def index():
    if "userName" in session:
        return redirect(url_for("user"))

    languageList = list(getLanguageList().keys())
    return render_template("index.html", languageList = languageList)


@app.route('/', methods=['POST', 'GET'])
def login():
    username = request.form['userName'].title()
    language = request.form['language']
    session["userName"] = username.title()
    session["language"] = language
    

    jsonFile = open("languages.json", "r")
    langDict = json.load(jsonFile) 
    jsonFile.close()

    
    langDict[username] = language

    with open('languages.json', 'w', encoding='utf-8') as f:
        json.dump(langDict, f, ensure_ascii=False, indent=4)

    return redirect(url_for("user"))

@app.route('/messages')
def user():
    if "userName" in session:
        userName = session["userName"]
        language = session["language"]
        messages = getMessages()
       
        # original = getMessages()
        # original = len(original)

        # f = open("info.txt", "w")
        # f.write(str(original))
        # f.close()


        return render_template("messages.html", userName = userName.title(), language = language, messages = messages)
    else:
        return render_template("index.html")

@app.route('/messages', methods=['POST'])
def message():

    userName = session["userName"] 
    message = request.form['message']

    # jsonFile = open("languages.json", "r")
    # lang = json.load(jsonFile) 
    # jsonFile.close()

    
    # del lang[userName]

    #language = list(lang.values())[0]

    sendMessage(userName, message)

    return redirect(url_for("user"))
    

@app.route("/logout")
def logout():
    session.pop("userName", None)
    session.pop("language", None)
    return redirect(url_for("index"))

@app.route("/logout", methods=['POST'])
def leave():
    return redirect(url_for("logout"))


# @app.route("/getData")
# def getData():
#     if "userName" in session:
#         userName = session["userName"]
#         language = session["language"]
#         messages = getMessages()
#         return messages

# def checkUpdates():

#     f = open("info.txt", "r")
#     original = f.read()
#     original = int(original)

    
#     new = getMessages()
#     new = len(new)

#     if new != original:
#         with app.test_request_context():
#             return redirect(url_for("login"))
    

    



if __name__ == "__main__":
    # scheduler = APScheduler()
    # scheduler.add_job(func=checkUpdates, trigger='interval', id='job', seconds=1)
    # scheduler.start()
    app.run(debug=1, host='192.168.2.180')
