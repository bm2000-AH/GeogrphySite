from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geography_site_1804'

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


@app.route('/guess_capitals', methods=['GET', 'POST'])
def guess_capitals():
    if 'score' not in session:
        session['score'] = 0
        session['question'] = 0
        session['asked'] = []

    if session['question'] >= 5:
        score = session['score']
        session.clear()
        return render_template('result.html', score=score)

    countries = list(countries_and_capitals.keys())
    ostalis = list(set(countries) - set(session['asked']))
    country = random.choice(ostalis)
    correct_capital = countries_and_capitals[country]

    options = [correct_capital]
    while len(options) < 4:
        capital = random.choice(list(countries_and_capitals.values()))
        if capital not in options:
            options.append(capital)
    random.shuffle(options)

    if request.method == 'POST':
        selected = request.form.get('answer')
        if selected == session['correct']:
            session['score'] += 1
        session['question'] += 1
        session['asked'].append(session['current_country'])
        return redirect(url_for('guess_capitals'))

    session['correct'] = correct_capital
    session['current_country'] = country
    return render_template('capital_quiz.html', country=country, options=options)


@app.route('/')
def index():
    return redirect(url_for('list_prof'))


if __name__ == '__main__':
    app.run(port=8880, host='127.0.0.1')
