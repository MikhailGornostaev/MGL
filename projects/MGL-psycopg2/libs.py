from flask import abort, session, request
import re
import psycopg2
from werkzeug.security import generate_password_hash

connection = psycopg2.connect(dbname='user_42_db', user='user_42', password='123', host='159.69.151.133', port='5056')
cursor = connection.cursor()


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


def sql_action(pick, action):
    if pick == "anime":
        if action == "select":
            cursor.execute("""select title,rating from public.anime
                              where creator =(select id from public.users where login =%s) 
                              order by rating desc;""", [session['userLogged']])
            db_resp = cursor.fetchall()
            return db_resp
        elif action == "delete":
            cursor.execute("""delete from anime 
                             where title=%s and rating=%s 
                            and creator =(select id from public.users where login =%s)""",
                           (session['titleA'], session['ratingA'], session['userLogged']))
            connection.commit()
        elif action == "insert":
            postgres_insert_query = """ INSERT INTO public.anime 
                                        (title,rating,creator) 
                                        VALUES (%s,%s, (select id from public.users where login = %s));"""
            record_to_insert = (request.form['title'], request.form['rating'], session['userLogged'])
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
        elif action == "update":
            cursor.execute("""Update public.anime set title=(%s), rating=(%s)
                              where title =(%s) and rating =(%s)""",
                           (request.form['title'], request.form['rating'], session['titleA'], session['ratingA']))
            connection.commit()
        else:
            abort(400)
    elif pick == "games":
        if action == "select":
            cursor.execute("""select title,rating from public.games
                              where creator =(select id from public.users where login =%s) 
                              order by rating desc;""", [session['userLogged']])
            db_resp = cursor.fetchall()
            return db_resp
        elif action == "delete":
            cursor.execute("""delete from games 
                             where title=%s and rating=%s 
                            and creator =(select id from public.users where login =%s)""",
                           (session['titleG'], session['ratingG'], session['userLogged']))
            connection.commit()
        elif action == "insert":
            postgres_insert_query = """ INSERT INTO public.games 
                                        (title,rating,creator) 
                                        VALUES (%s,%s, (select id from public.users where login = %s));"""
            record_to_insert = (request.form['title'], request.form['rating'], session['userLogged'])
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
        elif action == "update":
            cursor.execute("""Update public.games set title=(%s), rating=(%s)
                              where title =(%s) and rating =(%s)""",
                           (request.form['title'], request.form['rating'], session['titleG'], session['ratingG']))
            connection.commit()
        else:
            abort(400)
    elif pick == "registration":
        if action == "unique":
            cursor.execute("""select id from public.users
                              where login = %s or nick = %s or email = %s;""",
                           [request.form['login'], request.form['nick'], request.form['email']])
            db_resp = cursor.fetchall()
            return db_resp
        elif action == "insert":
            postgres_insert_query = """ INSERT INTO public.users 
                                        (nick, login, password, email) 
                                        VALUES (%s,%s,%s,%s)"""
            record_to_insert = (request.form['nick'], request.form['login'],
                                generate_password_hash(request.form['password']), request.form['email'])
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
    elif pick == "login":
        if action == "check":
            cursor.execute("""select password from public.users
                                      where login = %s""", [request.form['login']])
            db_resp = cursor.fetchall()
            return db_resp
    elif pick == "nickname":
        if action == "get":
            cursor.execute("""select nick from public.users
                                      where login = %s""", [session['userLogged']])
            db_resp = cursor.fetchall()
            nickname = db_resp[0][0]
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

