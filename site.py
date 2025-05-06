from datetime import datetime
from flask import Flask, redirect, url_for
from data import db_session
from flask import render_template
from data.tabl import Tabls
from data.users import User
from forms.user import RegisterForm, LoginForm
from forms.gamers import GamerForm
from flask_login import LoginManager, login_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Tabls).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
def index():
    """db_sess = db_session.create_session()
    jobs = db_sess.query(Tabls).all()
    return render_template("index.html", jobs=jobs)"""
    return f"""<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">

                        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
                        <link rel="stylesheet" type="text/css" href="../static/css/style.css"/>
      </head>
                        <title>Информация</title>
                      </head>
                      <body>
                        <h1><p align="center">Этот сайт посвящён игре "GeoGuessr"</p></h1>
                        <img src="img/emb.webp alt="Фото"" 
               alt="здесь должна была быть картинка, но не нашлась">

                        <p>GeoGuessr — браузерная игра, разработанная шведским программистом Антоном Валленом. Выпущена 9 мая 2013 года. В игре используются карты Google Street View, игроку требуется угадать своё местоположение в мире на карте Google Maps.</p>
                        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" 
                        integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" 
                        crossorigin="anonymous"></script>
                      </body>
                    </html>"""


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run()


if __name__ == '__main__':
    main()