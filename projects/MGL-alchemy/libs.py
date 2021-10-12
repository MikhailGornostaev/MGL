from flask import abort, session, request
import re
from base_con import db
from werkzeug.security import generate_password_hash


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(500), unique=False, nullable=False)
    nick = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    games = db.relationship('Games', backref='play')
    anime = db.relationship('Anime', backref='watch')

    def __init__(self, login, password, nick, email):
        self.login = login
        self.password = password
        self.nick = nick
        self.email = email


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(73), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, rating, creator):
        self.title = title
        self.rating = rating
        self.creator = creator


class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256),  nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, rating, creator):
        self.title = title
        self.rating = rating
        self.creator = creator


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


def alchemy_action(pick, action):
    if pick == 'login' and action == 'check':
        db_resp = Users.query.filter_by(login=request.form['login']).first()
        return db_resp

    elif pick == 'registration':

        p_word = generate_password_hash(request.form['password'])
        nick_name = request.form['nick']
        log_in = request.form['login']
        e_mail = request.form['email']

        if action == 'unique':
            db1 = Users.query.filter_by(nick=nick_name).first()
            db2 = Users.query.filter_by(login=log_in).first()
            db3 = Users.query.filter_by(email=e_mail).first()
            if db1 or db2 or db3 is not None:
                return True
            else:
                return False
        elif action == 'add':
            user = Users(log_in, p_word, nick_name, e_mail)
            db.session.add(user)
            db.session.commit()
        else:
            abort(400)

    elif pick == 'user' and action == 'nick':
        u_name = Users.query.filter_by(login=session['userLogged']).first().nick
        return u_name

    elif pick == "anime":

        log_in = session['userLogged']
        u_id = Users.query.filter_by(login=log_in).first().id

        if action == 'select':
            a_select = Anime.query.order_by(Anime.rating.desc()).filter_by(creator=u_id).all()
            db_resp = []
            for element in a_select:
                db_resp.append((element.title, element.rating))
            return db_resp
        elif action == 'delete':
            to_delete = Anime.query.filter_by(title=session['titleA'], rating=session['ratingA'], creator=u_id).first()
            db.session.delete(to_delete)
            db.session.commit()
        elif action == 'new':
            title = request.form['title']
            rating = request.form['rating']
            post = Anime(title, rating, u_id)
            db.session.add(post)
            db.session.commit()
        elif action == 'red':
            to_update = Anime.query.filter_by(title=session['titleA'], rating=session['ratingA']).first()
            to_update.title = request.form['title']
            to_update.rating = request.form['rating']
            db.session.commit()
        else:
            abort(400)

    elif pick == 'games':

        log_in = session['userLogged']
        u_id = Users.query.filter_by(login=log_in).first().id

        if action == 'select':
            a_select = Games.query.order_by(Games.rating.desc()).filter_by(creator=u_id).all()
            db_resp = []
            for element in a_select:
                db_resp.append((element.title, element.rating))
            return db_resp
        elif action == 'delete':
            to_delete = Games.query.filter_by(title=session['titleG'], rating=session['ratingG'], creator=u_id).first()
            db.session.delete(to_delete)
            db.session.commit()
        elif action == 'new':
            title = request.form['title']
            rating = request.form['rating']
            post = Games(title, rating, u_id)
            db.session.add(post)
            db.session.commit()
        elif action == 'red':
            to_update = Games.query.filter_by(title=session['titleG'], rating=session['ratingG']).first()
            to_update.title = request.form['title']
            to_update.rating = request.form['rating']
            db.session.commit()
        else:
            abort(400)
    else:
        abort(400)
