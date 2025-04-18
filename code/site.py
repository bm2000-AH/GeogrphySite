from flask import Flask, render_template, redirect
from loginform import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geography_site_1804'

@app.route('/<word>')
@app.route('/index/<word>')
def index(word):
    pass


@app.route('/training/<prof>')
def training(prof):
    pass

@app.route('/list_prof/<list>')
def list_prof(list):
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


if __name__ == '__main__':
    app.run(port=8880, host='127.0.0.1')