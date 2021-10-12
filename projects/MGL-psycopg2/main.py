from flask import Flask, render_template, url_for, request, redirect, abort, flash, session
from werkzeug.security import check_password_hash
from libs import reg_validation, content_validation, sql_action, post_getter
import psycopg2


app = Flask(__name__)
app.config['SECRET_KEY'] = 'e25a30bfb3e19e769cf8b5c0c024056be5162002'
connection = psycopg2.connect(dbname='user_42_db', user='user_42', password='123', host='159.69.151.133', port='5056')
cursor = connection.cursor()


@app.route("/main_page")
def main_page():
    return render_template("main.html")


@app.route("/")
def main_redirect():
    return redirect(url_for("main_page"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if 'userLogged' in session:
        return redirect(url_for("user"))
    elif request.method == "POST":
        if connection:
            db_resp = sql_action("login", "check")
            if len(db_resp) != 0:
                pass_get = db_resp[0][0]
                if check_password_hash(pass_get, request.form['password']):
                    session['userLogged'] = request.form['login']
                    return redirect(url_for("user"))
                else:
                    return redirect(url_for('login')), flash('Некорректный пароль', category='error')
            else:
                return redirect(url_for('login')), flash('Такого пользователя не существует', category='error')
    return render_template("login_page.html")


@app.route("/logout")
def logout():
    if 'userLogged' in session:
        del session['userLogged']
    else:
        return abort(403)
    return render_template("logout.html")


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        if reg_validation():
            return redirect(url_for("registration")), flash('Некорректные данные', category='high-error')
        else:
            if connection:
                db_resp = sql_action("registration", "unique")
                if len(db_resp) != 0:
                    return redirect(url_for("registration")), \
                           flash('Пользователь с такими данными существует', category='high-error')
                else:
                    session['reg'] = True
                    sql_action("registration", "insert")
            return redirect(url_for("complete"))

    return render_template("registration.html")


@app.route("/complete")
def complete():
    if 'reg' in session:
        return render_template("reg_success.html")
    else:
        abort(403)


@app.route("/user")
def user():
    if 'userLogged' in session:
        n = sql_action("nickname", "get")
        return render_template("user_page.html", usernick=n)
    else:
        return redirect(url_for("login"))


@app.route("/anime_list", methods=["GET", "POST", "DELETE"])
def anime_list():
    db_resp = None
    if 'userLogged' in session:
        if connection:
            db_resp = sql_action("anime", "select")
            if request.method == "POST":
                post_getter("anime")
            elif request.method == "DELETE":
                sql_action("anime", "delete")
    else:
        return redirect(url_for('login'))
    return render_template("anime_list.html", list=db_resp)


@app.route("/anime_new", methods=["GET", "POST"])
def anime_new():
    if 'userLogged' not in session:
        return redirect(url_for("login"))
    elif request.method == "POST":
        if content_validation("anime"):
            return redirect(url_for('anime_new')), flash('Некорректные данные', category='error')
        else:
            if connection:
                sql_action("anime", "insert")
            return redirect(url_for("anime_list")), flash('Запись добавлена успешно', category='high-success')
    else:
        return render_template("new_anime.html")


@app.route("/anime_red", methods=["GET", "POST"])
def anime_red():
    if 'userLogged' and 'titleA' and 'ratingA' in session:
        if request.method == "POST":
            if content_validation("anime"):
                return redirect(url_for('anime_new')), flash('Некорректные данные', category='error')
            elif connection:
                sql_action("anime", "update")
                return redirect(url_for("anime_list")), flash('Запись изменена успешно', category='high-success')
        return render_template("anime_red.html", title=session['titleA'], rating=session['ratingA'])
    else:
        abort(403)


@app.route("/game_list", methods=["GET", "POST", "DELETE"])
def game_list():
    db_resp = None
    if 'userLogged' in session:
        if connection:
            db_resp = sql_action("games", "select")
            if request.method == "POST":
                post_getter("games")
            elif request.method == "DELETE":
                sql_action("games", "delete")
    else:
        return redirect(url_for('login'))
    return render_template("game_list.html", list=db_resp)


@app.route("/game_new", methods=["GET", "POST"])
def game_new():
    if 'userLogged' not in session:
        return redirect(url_for("login"))
    elif request.method == "POST":
        if content_validation("games"):
            return redirect(url_for('game_new')), flash('Некорректные данные', category='error')
        else:
            if connection:
                sql_action("games", "insert")
            return redirect(url_for("game_list")), flash('Запись добавлена успешно', category='high-success')
    else:
        return render_template("new_game.html")


@app.route("/game_red", methods=["GET", "POST"])
def game_red():
    if 'userLogged' and 'titleG' and 'ratingG' in session:
        if request.method == "POST":
            if content_validation("games"):
                return redirect(url_for('game_new')), flash('Некорректные данные', category='error')
            elif connection:
                sql_action("games", "update")
                return redirect(url_for("game_list")), flash('Запись изменена успешно', category='high-success')
        return render_template("game_red.html", title=session['titleG'], rating=session['ratingG'])
    else:
        abort(403)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403


if __name__ == "__main__":
    app.run(debug=True)
