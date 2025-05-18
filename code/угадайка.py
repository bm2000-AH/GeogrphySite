from flask import Flask, render_template, request, redirect, url_for, session
import random
from data import db_session
import requests
from datetime import datetime
import csv
from data.tabl import Tabls
from data.users import User
from forms.user import RegisterForm, LoginForm
from forms.gamers import GamerForm
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_login import current_user

db_session.global_init("db/names.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geography_site_1804'

flags_data = []

with open('flags_extended.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) == 2:
            country, code = row
            flags_data.append((country.strip(), code.strip()))

countries_and_capitals = {
    'Россия': 'Москва',
    'Франция': 'Париж',
    'Германия': 'Берлин',
    'Италия': 'Рим',
    'Испания': 'Мадрид',
    'Великобритания': 'Лондон',
    'Япония': 'Токио',
    'Китай': 'Пекин',
    'Индия': 'Нью-Дели',
    'Бразилия': 'Бразилиа',
    'США': 'Вашингтон',
    'Канада': 'Оттава',
    'Австралия': 'Канберра',
    'Мексика': 'Мехико',
    'Аргентина': 'Буэнос-Айрес',
    'Южная Корея': 'Сеул',
    'Новая Зеландия': 'Уэллингтон',
    'Южноафриканская Республика': 'Претория',
    'Норвегия': 'Осло',
    'Швеция': 'Стокгольм',
    'Финляндия': 'Хельсинки',
    'Дания': 'Копенгаген',
    'Ирландия': 'Дублин',
    'Португалия': 'Лиссабон',
    'Греция': 'Афины',
    'Турция': 'Анкара',
    'Исландия': 'Рейкьявик',
    'Чехия': 'Прага',
    'Польша': 'Варшава',
    'Австрия': 'Вена',
    'Швейцария': 'Берн',
    'Бельгия': 'Брюссель',
    'Нидерланды': 'Амстердам',
    'Люксембург': 'Люксембург',
    'Словакия': 'Братислава',
    'Албания': 'Тирана',
    'Алжир': 'Алжир',
    'Ангола': 'Луанда',
    'Антигуа и Барбуда': 'Сент-Джонс',
    'Армения': 'Ереван',
    'Афганистан': 'Кабул',
    'Багамские Острова': 'Нассау',
    'Бангладеш': 'Дакка',
    'Барбадос': 'Бриджтаун',
    'Белиз': 'Бельмопан',
    'Бенин': 'Порто-Ново',
    'Болгария': 'София',
    'Босния и Герцеговина': 'Сараево',
    'Ботсвана': 'Габороне',
    'Буркина-Фасо': 'Уагадугу',
    'Вануату': 'Порт-Вила',
    'Венгрия': 'Будапешт',
    'Гайана': 'Демерара-Ривер',
    'Гренада': "Сент-Джорджес",
    'Грузия': "Тбилиси",
    'Джибути': "Джибути",
    'Доминика': "Розо",
    'Египет': "Каир",
    'Замбия': "Лусака",
    'Зимбабве': "Хараре",
    'Ирак': "Багдад",
    'Иран': "Тегеран",
    'Кабо-Верде': "Прая",
    'Катар': "Доха",
    'Кения': "Найроби",
    'Кипр': "Никосия",
    'Киргизия': "Бишкек",
    'Коста-Рика': "Сан-Хосе",
    'Латвия': "Рига",
    'Ливан': "Бейрут",
    'Ливия': "Триполи"
}


@app.route('/list_prof')
def list_prof():
    return render_template('menu.html')



@app.route('/game/capitals', methods=['GET', 'POST'])
def guess_capitals():
    if 'score' not in session:
        session['score'] = 0
        session['question'] = 0
        session['asked'] = []

    countries = list(countries_and_capitals.keys())
    country = random.choice(countries)

    while country in session['asked']:
        country = random.choice(countries)

    correct_capital = countries_and_capitals[country]
    capitals = list(countries_and_capitals.values())
    options = random.sample([c for c in capitals if c != correct_capital], 3)
    options.append(correct_capital)
    random.shuffle(options)

    if request.method == 'POST':
        user_guess = request.form.get('capital')
        correct_capital = request.form.get('correct_capital')
        is_correct = user_guess == correct_capital
        if is_correct:
            session['score'] += 1
        session['question'] += 1
        session['asked'].append(request.form.get('country'))

        if session['question'] == 5:
            score = session['score']
            if current_user.is_authenticated:
                db_sess = db_session.create_session()
                user = db_sess.get(User, current_user.id)
                user.score += score
                db_sess.commit()
            session.pop('score')
            session.pop('question')
            session.pop('asked')
            return render_template('result.html', score=score)

    return render_template('capital_quiz.html', country=country, options=options, correct_capital=correct_capital)


coords_city = [
    (55.7558, 37.6176, "Москва"),
    (48.8566, 2.3522, "Париж"),
    (52.5200, 13.4050, "Берлин"),
    (41.9028, 12.4964, "Рим"),
    (40.4168, -3.7038, "Мадрид"),
    (51.5074, -0.1278, "Лондон"),
    (35.6895, 139.6917, "Токио"),
    (39.9042, 116.4074, "Пекин"),
    (28.6139, 77.2090, "Нью-Дели"),
    (38.9072, -77.0369, "Вашингтон"),
    (45.4215, -75.6995, "Оттава"),
    (35.6762, 139.6503, "Осака"),
    (37.7749, -122.4194, "Сан-Франциско"),
    (40.7128, -74.0060, "Нью-Йорк"),
    (34.0522, -118.2437, "Лос-Анджелес"),
    (48.2082, 16.3738, "Вена"),
    (59.3293, 18.0686, "Стокгольм"),
    (60.1699, 24.9384, "Хельсинки"),
    (59.9139, 10.7522, "Осло"),
    (50.8503, 4.3517, "Брюссель"),
    (52.3676, 4.9041, "Амстердам"),
    (46.2044, 6.1432, "Женева"),
    (41.7151, 44.8271, "Тбилиси"),
    (25.276987, 55.296249, "Дубай"),
    (21.0278, 105.8342, "Ханой"),
    (13.7563, 100.5018, "Бангкок"),
    (31.7683, 35.2137, "Иерусалим"),
    (32.0853, 34.7818, "Тель-Авив"),
    (6.5244, 3.3792, "Лагос"),
    (33.5731, -7.5898, "Касабланка"),
    (30.0444, 31.2357, "Каир"),
    (24.7136, 46.6753, "Эр-Рияд"),
    (35.6892, 51.3890, "Тегеран"),
    (33.3128, 44.3615, "Багдад"),
    (41.0082, 28.9784, "Стамбул"),
    (39.9334, 32.8597, "Анкара"),
    (37.9838, 23.7275, "Афины"),
    (42.6977, 23.3219, "София"),
    (47.4979, 19.0402, "Будапешт"),
    (50.0755, 14.4378, "Прага"),
    (51.1657, 10.4515, "Германия"),
    (53.3498, -6.2603, "Дублин"),
    (38.7223, -9.1393, "Лиссабон"),
    (64.9631, -19.0208, "Исландия"),
    (35.8617, 104.1954, "Китай"),
    (19.4326, -99.1332, "Мехико"),
    (4.7110, -74.0721, "Богота"),
    (12.9716, 77.5946, "Бангалор"),
    (23.8103, 90.4125, "Дакка"),
    (14.5995, 120.9842, "Манила"),
    (31.2304, 121.4737, "Шанхай"),
    (43.6532, -79.3832, "Торонто"),
    (35.8617, 104.1954, "Ухань"),
    (37.5665, 126.9780, "Сеул"),
    (22.3964, 114.1095, "Гонконг"),
    (35.0116, 135.7681, "Киото"),
    (1.3521, 103.8198, "Сингапур"),
    (55.9533, -3.1883, "Эдинбург"),
    (53.4808, -2.2426, "Манчестер"),
    (52.4862, -1.8904, "Бирмингем"),
    (45.5017, -73.5673, "Монреаль"),
    (10.8231, 106.6297, "Хошимин"),
    (50.1109, 8.6821, "Франкфурт"),
    (43.7102, 7.2620, "Ницца"),
    (35.8617, 104.1954, "Сиань"),
    (19.075983, 72.877655, "Мумбаи"),
    (6.9271, 79.8612, "Коломбо"),
    (36.2048, 138.2529, "Нагоя"),
    (60.4720, 8.4689, "Тронхейм"),
    (50.0647, 19.9450, "Краков"),
    (39.9526, -75.1652, "Филадельфия"),
    (29.7604, -95.3698, "Хьюстон"),
    (35.7796, -78.6382, "Роли"),
    (41.2565, -95.9345, "Омаха"),
    (33.4484, -112.0740, "Финикс"),
    (47.6062, -122.3321, "Сиэтл"),
    (38.2527, -85.7585, "Луисвилл"),
    (30.2672, -97.7431, "Остин"),
    (36.1627, -86.7816, "Нашвилл"),
    (44.9778, -93.2650, "Миннеаполис"),
    (39.9612, -82.9988, "Коламбус"),
    (35.9940, -78.8986, "Дарем"),
    (42.3601, -71.0589, "Бостон"),
    (32.7767, -96.7970, "Даллас"),
    (33.7490, -84.3880, "Атланта"),
    (36.1627, -86.7816, "Нашвилл"),
    (43.0389, -87.9065, "Милуоки"),
    (39.7392, -104.9903, "Денвер"),
    (25.7617, -80.1918, "Майами")
]


def get_valid_coordinates():
    return random.choice(coords_city)


@app.route('/guess_map', methods=['GET', 'POST'])
def guess_map():
    if request.method == 'POST':
        user_guess = request.form['guess'].strip().lower()
        correct_city = session.get('correct_city', '').lower()



        is_correct = user_guess == correct_city
        return render_template('map_result.html', is_correct=is_correct,
                               correct_city=session.get('correct_city'),
                               user_guess=user_guess)

    lat, lon, city = get_valid_coordinates()

    map_url = f"https://static-maps.yandex.ru/1.x/?ll={lon},{lat}&z=14&size=600,400&l=map"

    session['correct_city'] = city
    return render_template('map_guess.html', map_url=map_url)


@app.route('/guess_flags', methods=['GET', 'POST'])
def guess_flags():
    if 'score_flags' not in session:
        session['score_flags'] = 0
        session['question_flags'] = 0
        session['asked_flags'] = []

    if session['question_flags'] == 5:
        score = session['score_flags']
        if current_user.is_authenticated:
            db_sess = db_session.create_session()
            user = db_sess.get(User, current_user.id)
            user.score += score
            db_sess.commit()
        session.pop('score_flags')
        session.pop('question_flags')
        session.pop('asked_flags')
        return render_template('result.html', score=score)

    options = [item for item in flags_data if item[0] not in session['asked_flags']]
    country, code = random.choice(options)
    correct_country = country

    answer_options = [correct_country]
    while len(answer_options) < 4:
        option = random.choice(flags_data)[0]
        if option not in answer_options:
            answer_options.append(option)
    random.shuffle(answer_options)

    if request.method == 'POST':
        selected = request.form.get('answer')
        if selected == session.get('correct_flag_country'):
            session['score_flags'] += 1
        session['question_flags'] += 1
        session['asked_flags'].append(session['correct_flag_country'])
        return redirect(url_for('guess_flags'))

    session['correct_flag_country'] = correct_country
    flag_url = f"https://flagcdn.com/w320/{code.lower()}.png"
    return render_template('flag_quiz.html', flag_url=flag_url, options=answer_options)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    print("ok")
    form = GamerForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            print("nice")
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            print("nm")
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        print("pri")
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/list_prof')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/leaders')
def show_leaders():
    db_sess = db_session.create_session()
    leaders = db_sess.query(User).filter(User.score > 0).order_by(User.score.desc()).limit(10).all()

    results = [(user.name, user.score) for user in leaders]

    return render_template('leaders.html', results=results)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/list_prof")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    return render_template('base.html', title='Главная страница')


def main():
    db_session.global_init("db/names.db")
    app.run()


if __name__ == '__main__':
    app.run(port=8881, host='127.0.0.1')