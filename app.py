from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/shahzod'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
app.config['UPLOAD_FOLDER'] = 'static/img'
app.config['SECRET_KEY'] = 'aaaa'
db = SQLAlchemy(app)
ALLOWED_EXTESION = {'png', 'jpg', 'jpeg'}


class Users(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    photo = Column(String)


with app.app_context():
    db.create_all()


def current_user():
    user_now = None
    if 'username' in session:
        user_get = Users.query.filter(Users.name == session['username']).first()
        user_now = user_get

    return user_now


def users_folder():
    upload_folder = 'static/img/'
    return upload_folder


def checkFile(filename):
    value = '.' in filename
    type_file = filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTESION
    return value and type_file

#    0     1
# [search.png]

@app.route('/', methods=["POST", "GET"])
def hello_world():  # put application's code here
    user = current_user()
    if request.method == "POST":
        name = request.form.get('name')
        surname = request.form.get('surname')
        password = request.form.get('password')
        hashed = generate_password_hash(password=password, method='sha256')
        Users.query.filter(Users.id == user.id).update({
            "name": name,
            "surname": surname,
            "password": hashed
        })
        db.session.commit()
    return render_template('index.html', user=user)


@app.route('/basic')
def basic():
    return render_template('../FIGMA/novosti.html')


news = []

@app.route('/index')
def index():
        return render_template('profile.html')
@app.route('/panel', methods=["POST", "GET"])
def panel():
    if request.method == "POST":
        name = request.form.get('news')
        about = request.form.get('name')
        data = request.form.get('data')
        shahzod = {'name': name, 'about': about, 'data': data}
        news.append(shahzod)
        print(news)
        return redirect(url_for('panel'))
    return render_template('panel.html', news=news)


users = []
kor = []


@app.route('/kat', methods=["POST", "GET"])
def kat():
    if request.method == "POST":
        name = request.form.get('nomi')
        about = request.form.get('narxi')
        data = request.form.get('rasmi')
        kor2 = {'name': name, 'about': about, 'data': data}
        kor.append(kor2)
        print(kor)
        return redirect(url_for('kat'))
    return render_template('korzina.html', korzina=kor)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        username = Users.query.filter(Users.name == name).first()
        if username:
            if check_password_hash(username.password, password):
                session["username"] = username.name
                return redirect(url_for('hello_world'))
            else:
                return render_template('login.html', error='Username or password incorect')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session['username'] = ""
    return redirect(url_for('login'))


@app.route('/reg', methods=["POST", "GET"])
def reg():
    if request.method == "POST":
        name = request.form.get('name')
        surname = request.form.get('surname')
        password = request.form.get('password')
        photo = request.files['photo']
        folder = users_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file))
        hashed = generate_password_hash(password=password, method='sha256')
        add = Users(name=name, surname=surname, password=hashed, photo=photo_url)
        db.session.add(add)
        db.session.commit()

        return redirect(url_for('reg'))
    return render_template('reg.html', )


if __name__ == '__main__':
    app.run()
