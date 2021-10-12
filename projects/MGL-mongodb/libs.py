from flask import abort, session, request
import re
import psycopg2
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

connection = psycopg2.connect(dbname='user_42_db', user='user_42', password='123', host='159.69.151.133', port='5056')
cursor = connection.cursor()

cluster = MongoClient("mongodb+srv://user_42:123@cluster0.2uyq0.mongodb.net/geek_list?retryWrites=true&w=majority")
db = cluster["geek_list"]
collection = db["users"]


def reg_validation():
    nick = request.form['nick']
    login = request.form['login']
    password = request.form['password']
    email = request.form['email']
    if (nick == ""
            or len(nick) <= 1
            or len(nick) >= 16
            or re.search(r'[.!"`\'#%&,:;<>=@{}~$()*+/\\?\[\]^|А-я]', nick)
            or login == ""
            or len(login) <= 4
            or len(login) >= 16
            or re.search(r'[\-._!"`\'#%&,:;<>=@{}~$()*+/\\?\[\]^|А-я]', login)
            or password == ""
            or len(password) <= 5
            or len(password) >= 21
            or not re.search(r'[-_*#\[\]|A-z0-9]', password)
            or email == ""
            or len(email) <= 6
            or len(email) >= 51):
        return True
    else:
        return False


def content_validation(pick):
    title = request.form['title']
    rating = request.form['rating']
    if pick == "anime":
        if (title == ""
                or len(title) <= 3
                or len(title) >= 257
                or re.search(r'[._!"#%&,:;<>=@{}~$()*+/\\?\[\]^|]', title)
                or rating not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')):
            return True
        else:
            return False
    elif pick == "games":
        if (title == ""
                or len(title) <= 1
                or len(title) >= 73
                or re.search(r'[._!"#%&,:;<>=@{}~$()*+/\\?\[\]^|]', title)
                or rating not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')):
            return True
        else:
            return False


def mongo_action(pick, action):
    if pick == "anime":
        if action == "select":
            db_resp = collection.find_one({"login": session['userLogged']})["anime"]
            return db_resp
        elif action == "delete":
            collection.update({"login": session["userLogged"]},
                              {"$pull": {'anime': (session['titleA'], int(session['ratingA']))}})
        elif action == "insert":
            post = (request.form['title'], int(request.form['rating']))
            collection.update_one({"login": session['userLogged']}, {"$addToSet": {'anime': post}})
        elif action == "update":
            collection.update_one({"login": "login2", "anime": (session['titleA'], int(session['ratingA']))},
                                  {"$set": {"anime.$": (request.form['title'], int(request.form['rating']))}})
        else:
            abort(400)
    elif pick == "games":
        if action == "select":
            db_resp = collection.find_one({"login": session['userLogged']})["games"]
            return db_resp
        elif action == "delete":
            collection.update({"login": session["userLogged"]},
                              {"$pull": {'games': (session['titleG'], int(session['ratingG']))}})
        elif action == "insert":
            post = (request.form['title'], int(request.form['rating']))
            collection.update_one({"login": session['userLogged']}, {"$addToSet": {'games': post}})
        elif action == "update":
            collection.update_one({"login": "login2", "games": (session['titleG'], int(session['ratingG']))},
                                  {"$set": {"games.$": (request.form['title'], int(request.form['rating']))}})
        else:
            abort(400)
    elif pick == "registration":
        if action == "unique":
            take1 = collection.find_one({"login": request.form['login']})
            take2 = collection.find_one({"nick": request.form['nick']})
            take3 = collection.find_one({"email": request.form['email']})
            if take1 or take2 or take3 is not None:
                return True
            else:
                return False
        elif action == "insert":
            user = {
                "nickname": request.form['nick'],
                "login": request.form['login'],
                "password": generate_password_hash(request.form['password']),
                "email": request.form['email'],
                "anime": [],
                "games": []
            }
            collection.insert_one(user)
    elif pick == "login":
        if action == "check":
            db_resp = collection.find_one({"login": request.form['login']})
            return db_resp
    elif pick == "nickname":
        if action == "get":
            db_resp = collection.find_one({"login": session['userLogged']})
            nickname = db_resp['nickname']
            return nickname
    else:
        abort(400)


def post_getter(pick):
    if pick == "anime":
        post_formed = list(request.form)
        post_split = post_formed[0].split('.' * 169)
        session['titleA'] = post_split[0]
        session['ratingA'] = post_split[1]
    elif pick == "games":
        post_formed = list(request.form)
        post_split = post_formed[0].split('.' * 169)
        session['titleG'] = post_split[0]
        session['ratingG'] = post_split[1]
    else:
        abort(400)
